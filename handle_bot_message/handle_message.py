import sys

import telegram
from telegram.error import Unauthorized, BadRequest

from Session import Session
from form_handling import RequestToStart, resolve_form_step, RequestLanguage, HomeStep, DonationStatus, AboutCampaign
from localization import localize, make_a_new_donation_message_id, donation_status_message_id, about_campaign_message_id
from session_handling import get_session, update_session
from telegram_bot import get_bot


def handle_message(update: telegram.Update):
    if update is None or update.message is None:
        return

    if update.message.from_user is None or update.message.from_user.is_bot:
        return

    try:
        handle_core(update)
    except Unauthorized as e:
        print(f"Unauthorized: {e}", file=sys.stderr)
    except BadRequest as e:
        print(f"Bad request: {e}", file=sys.stderr)


def handle_core(update: telegram.Update):
    session = get_session(update.message.chat_id)
    form_step = None

    if message_is_start_cmd(session, update.message.text):
        session.form_step = RequestToStart.__name__

    if message_is_donation_status_cmd(session, update.message.text):
        session.form_step = DonationStatus.__name__

    if message_is_about_campaign_cmd(session, update.message.text):
        session.form_step = AboutCampaign.__name__

    if message_is_change_language_cmd(session, update.message.text):
        form_step = RequestLanguage(get_bot(), HomeStep.__name__)

    if form_step is None:
        form_step = resolve_form_step(session.form_step, get_bot())
    next_step_name = form_step.handle(update)

    next_step = resolve_form_step(next_step_name, get_bot())
    next_step.request(update)

    session = get_session(update.message.chat_id)
    session.form_step = type(next_step).__name__
    update_session(session)


def message_is_start_cmd(session: Session, message: str):
    return message in ['/start', '/new_donation', localize(session, make_a_new_donation_message_id)]


def message_is_donation_status_cmd(session: Session, message: str):
    return message in ['/donation_status', localize(session, donation_status_message_id)]


def message_is_about_campaign_cmd(session: Session, message: str):
    return message in ['/about_campaign', localize(session, about_campaign_message_id)]


def message_is_change_language_cmd(session: Session, message: str):
    return message in ['/change_language']
