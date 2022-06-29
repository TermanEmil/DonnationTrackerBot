import os
import re
from abc import ABC
from datetime import datetime

import pytz
import telegram
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

from attachements import upload_attachment, AttachmentException
from localization import localize, request_screenshot_message_id, localize_random_thank_you, \
    request_contacts_message_id, no_need_for_confirmation_message_id, invalid_email_message_id, \
    donation_status_message_id, about_campaign_message_id, make_a_new_donation_message_id, \
    thanks_for_contacts_message_id, you_did_not_upload_confirmation_message_id, you_did_not_share_a_contact_message_id, \
    donation_status_first_day_message_id, donation_status_after_24h_message_id, donation_status_after_1week_message_id, \
    campaign_message_id, type_start_to_start_message_id, photo_not_attached_message_id, \
    request_a_new_donation_message_id, payment_details_message_id, quick_payment_message_id
from session_handling import get_session, update_session
from spreadsheets import add_to_spreadsheet_last_upload_data
from telegram_bot import get_bot


class FormStep(ABC):
    def request(self, update: telegram.Update):
        pass

    def handle(self, update: telegram.Update) -> str:
        raise


class RequestToStart(FormStep):
    def __init__(self, bot: telegram.Bot):
        self.bot = bot

    def request(self, update: telegram.Update):
        session = get_session(update.message.chat_id)
        markup = ReplyKeyboardMarkup([["/start"]], one_time_keyboard=True, resize_keyboard=True)
        self.bot.send_message(
            update.message.chat_id,
            localize(session, type_start_to_start_message_id),
            reply_markup=markup)

    def handle(self, update: telegram.Update) -> str:
        if update.message.text not in ["/start"]:
            return self.__class__.__name__

        session = get_session(update.message.chat_id)
        if session.language is None:
            return RequestLanguage.__name__

        return RequestScreenshot.__name__


class RequestLanguage(FormStep):
    def __init__(self, bot: telegram.Bot):
        self.bot = bot

    def request(self, update: telegram.Update):
        markup = ReplyKeyboardMarkup([["UA", "ENG"]], one_time_keyboard=True, resize_keyboard=True)
        self.bot.send_message(
            update.message.chat_id,
            "Привіт, захисник(ця)! Будь ласка, обери мову\n"
            "---\n"
            "Hello, defender! Please choose the language\n",
            reply_markup=markup)

    def handle(self, update: telegram.Update) -> str:
        if update.message.text not in ["UA", "ENG"]:
            return self.__class__.__name__

        session = get_session(update.message.chat_id)
        session.language = update.message.text.lower()
        update_session(session)
        return RequestNewDonation.__name__


class RequestNewDonation(FormStep):
    def __init__(self, bot: telegram.Bot):
        self.bot = bot

    def request(self, update: telegram.Update):
        session = get_session(update.message.chat_id)

        self.bot.send_message(
            update.message.chat_id,
            localize(session, request_a_new_donation_message_id),
            reply_markup=None)

    def handle(self, update: telegram.Update) -> str:
        return HomeStep.__name__


class SharePaymentDetails(FormStep):
    def __init__(self, bot: telegram.Bot):
        self.bot = bot

    def request(self, update: telegram.Update):
        pass

    def handle(self, update: telegram.Update) -> str:
        session = get_session(update.message.chat_id)
        message = localize(session, payment_details_message_id)

        message = message.replace('{bank-card}', os.environ.get('BANK_CARD'))
        message = message.replace('{bank-iban}', os.environ.get('BANK_IBAN'))

        quick_payment_button = InlineKeyboardButton(
            text=localize(session, quick_payment_message_id),
            url=os.environ.get('QUICK_PAYMENT_LINK'))
        markup = InlineKeyboardMarkup(
            [[quick_payment_button]],
            one_time_keyboard=True,
            resize_keyboard=True)

        self.bot.send_message(
            update.message.chat_id,
            message,
            reply_markup=markup)
        return HomeStep.__name__


class RequestScreenshot(FormStep):
    def __init__(self, bot: telegram.Bot):
        self.bot = bot

    def request(self, update: telegram.Update):
        pass

    def handle(self, update: telegram.Update) -> str:
        session = get_session(update.message.chat_id)
        self.bot.send_message(
            update.message.chat_id,
            localize(session, request_screenshot_message_id),
            reply_markup=None)
        return HandleScreenshot.__name__


class HandleScreenshot(FormStep):
    def __init__(self, bot: telegram.Bot):
        self.bot = bot

    def request(self, update: telegram.Update):
        pass

    def handle(self, update: telegram.Update) -> str:
        session = get_session(update.message.chat_id)

        if update.message.photo is None or len(update.message.photo) == 0:
            self.bot.send_message(
                update.message.chat_id,
                str(localize(session, photo_not_attached_message_id)),
                reply_markup=None)
            return self.__class__.__name__

        try:
            file_name, url = upload_attachment(update.message.photo)
        except AttachmentException as e:
            self.bot.send_message(update.message.chat_id, str(e), reply_markup=None)
            return self.__class__.__name__

        session = get_session(update.message.chat_id)
        session.uploads += url + '\n'
        session.upload_date = datetime.now(tz=pytz.UTC).isoformat()
        update_session(session)

        message_text, image_url = localize_random_thank_you(session)
        get_bot().send_photo(update.message.chat_id, photo=image_url, caption=message_text)

        return RequestContacts.__name__


class RequestContacts(FormStep):
    def __init__(self, bot: telegram.Bot):
        self.bot = bot

    def request(self, update: telegram.Update):
        session = get_session(update.message.chat_id)

        options = [localize(session, no_need_for_confirmation_message_id)]
        if session.contact is not None:
            options.append(session.contact)

        markup = ReplyKeyboardMarkup(
            [options],
            one_time_keyboard=True,
            resize_keyboard=True)

        self.bot.send_message(
            update.message.chat_id,
            localize(session, request_contacts_message_id),
            reply_markup=markup)

    def handle(self, update: telegram.Update) -> str:
        session = get_session(update.message.chat_id)
        if update.message.text == localize(session, no_need_for_confirmation_message_id):
            markup = ReplyKeyboardMarkup(
                [[
                    localize(session, about_campaign_message_id),
                    localize(session, make_a_new_donation_message_id)
                ]],
                one_time_keyboard=True,
                resize_keyboard=True)
            self.bot.send_message(
                update.message.chat_id,
                localize(session, thanks_for_contacts_message_id),
                reply_markup=markup)
            return HomeStep.__name__

        mail_regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if update.message.text is None or not re.fullmatch(mail_regex, update.message.text):
            self.bot.send_message(
                update.message.chat_id,
                localize(session, invalid_email_message_id),
                reply_markup=None)
            return self.__class__.__name__

        session.contact = update.message.text
        update_session(session)

        markup = ReplyKeyboardMarkup(
            [[
                localize(session, donation_status_message_id),
                localize(session, about_campaign_message_id),
                localize(session, make_a_new_donation_message_id)
            ]],
            one_time_keyboard=True,
            resize_keyboard=True)
        self.bot.send_message(
            update.message.chat_id,
            localize(session, thanks_for_contacts_message_id),
            reply_markup=markup)

        add_to_spreadsheet_last_upload_data(session)
        return HomeStep.__name__


class DonationStatus(FormStep):
    def __init__(self, bot: telegram.Bot):
        self.bot = bot

    def request(self, update: telegram.Update):
        pass

    def handle(self, update: telegram.Update) -> str:
        session = get_session(update.message.chat_id)
        if session.upload_date is None:
            self.bot.send_message(
                update.message.chat_id,
                localize(session, you_did_not_upload_confirmation_message_id),
                reply_markup=None)
            return HomeStep.__name__

        if session.contact is None:
            self.bot.send_message(
                update.message.chat_id,
                localize(session, you_did_not_share_a_contact_message_id),
                reply_markup=None)
            return HomeStep.__name__

        last_upload = datetime.fromisoformat(session.upload_date)
        delta = datetime.now(tz=pytz.UTC) - last_upload

        if delta.days <= 0:
            message = localize(session, donation_status_first_day_message_id)
        elif delta.days < 7:
            message = localize(session, donation_status_after_24h_message_id)
        else:
            message = localize(session, donation_status_after_1week_message_id)

        self.bot.send_message(update.message.chat_id, message, reply_markup=None)
        return HomeStep.__name__


class AboutCampaign(FormStep):
    def __init__(self, bot: telegram.Bot):
        self.bot = bot

    def request(self, update: telegram.Update):
        pass

    def handle(self, update: telegram.Update) -> str:
        session = get_session(update.message.chat_id)
        self.bot.send_message(
            update.message.chat_id,
            localize(session, campaign_message_id),
            reply_markup=None)
        return HomeStep.__name__


class HomeStep(FormStep):
    def __init__(self, bot: telegram.Bot):
        self.bot = bot

    def request(self, update: telegram.Update):
        pass

    def handle(self, update: telegram.Update) -> str:
        pass


def resolve_form_step(
        form_step_name: str,
        bot: telegram.Bot) -> FormStep:
    if form_step_name == RequestToStart.__name__ or form_step_name == 'RequestToStart':
        return RequestToStart(bot)

    if form_step_name == RequestLanguage.__name__:
        return RequestLanguage(bot)

    if form_step_name == RequestNewDonation.__name__:
        return RequestNewDonation(bot)

    if form_step_name == SharePaymentDetails.__name__:
        return SharePaymentDetails(bot)

    if form_step_name == RequestScreenshot.__name__:
        return RequestScreenshot(bot)

    if form_step_name == RequestContacts.__name__:
        return RequestContacts(bot)

    if form_step_name == HomeStep.__name__:
        return HomeStep(bot)

    if form_step_name == DonationStatus.__name__:
        return DonationStatus(bot)

    if form_step_name == AboutCampaign.__name__:
        return AboutCampaign(bot)

    if form_step_name == HandleScreenshot.__name__:
        return HandleScreenshot(bot)

    return HomeStep(bot)
