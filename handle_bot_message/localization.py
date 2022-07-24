from typing import Tuple

from Session import Session
import random


request_screenshot_message_id = 'request_screenshot_message_id'
photo_not_attached_message_id = 'photo_not_attached_message_id'
thanks_for_upload_message_id = 'thanks_for_upload_message_id'
request_contacts_message_id = 'request_contacts_message_id'
no_need_for_confirmation_message_id = 'no_need_for_confirmation_message_id'
request_a_new_donation_message_id = 'request_a_new_donation_message_id'

thanks_for_contacts_message_id = 'thanks_for_contacts_message_id'

file_too_large_message_id = 'file_too_large_message_id'
invalid_email_message_id = 'invalid_email_message_id'

donation_status_message_id = 'donation_status_message_id'
about_campaign_message_id = 'about_campaign_message_id'
make_a_new_donation_message_id = 'make_a_new_donation_message_id'

you_did_not_upload_confirmation_message_id = 'you_did_not_upload_confirmation_message_id'
you_did_not_share_a_contact_message_id = 'you_did_not_share_a_contact_message_id'

donation_status_first_day_message_id = 'donation_status_first_day_message_id'
donation_status_after_24h_message_id = 'donation_status_after_24h_message_id'
donation_status_after_1week_message_id = 'donation_status_after_1week_message_id'

campaign_message_id = "campaign_message_id"

type_start_to_start_message_id = "type_start_to_start_message_id"

thanks_1_message_id = 'thanks_1_message_id'
thanks_2_message_id = 'thanks_2_message_id'
thanks_3_message_id = 'thanks_3_message_id'

payment_details_message_id = 'payment_details_message_id'
quick_payment_message_id = 'quick_payment_message_id'

_messages = {
    'eng': {
        request_screenshot_message_id: "Thank you for your donation! Let’s make a quick approval before you can see "
                                       "updates on your contribution. Please, send a screenshot of your payment",
        file_too_large_message_id: "File too large (max 10 MB)",
        invalid_email_message_id: "Invalid email format",
        request_contacts_message_id: "Please, tell us your mail address if you are willing to be confirmed on what "
                                     "your donation will be spent for and get its photo proves",
        no_need_for_confirmation_message_id: "I don’t need to be confirmed",
        thanks_for_contacts_message_id: "Thank you! You can check the status of your donation using /donation_status",

        photo_not_attached_message_id: "Photo not attached",
        request_a_new_donation_message_id: "In case you have already donated with us choose /attach_donation\n"
                                           "If you’re willing to donate choose /new_donation",

        donation_status_message_id: "Donation status",
        about_campaign_message_id: "About campaign",
        make_a_new_donation_message_id: "Make a new donation",

        you_did_not_upload_confirmation_message_id: "You did not upload a confirmation",
        you_did_not_share_a_contact_message_id: "You did not share a contact",

        donation_status_first_day_message_id: "Your donation is confirmed & will be transferred to our defenders",
        donation_status_after_24h_message_id: "Your donation was transferred to our defenders, the request is already "
                                              "performing",
        donation_status_after_1week_message_id: "Your donation made us one step closer to the victory. We will share "
                                                "photo proof on your email in a while. Thank you for your "
                                                "contribution!",

        campaign_message_id: "Campaign link here",

        type_start_to_start_message_id: "Type /start to start",

        thanks_1_message_id: "Wow! You've just shot the russian orc! Thank you for your donation!",
        thanks_2_message_id: "Thank you for investing in the peaceful future for Ukraine!",
        thanks_3_message_id: "By making this donation, you have confirmed your commitment to democratic values and "
                             "justice! Thank you! ",

        quick_payment_message_id: "Quick donation",
        payment_details_message_id: "Payment details\n"
                                    "\n"
                                    "Bank card: {bank-card}\n"
                                    "IBAN: {bank-iban}\n"
                                    "\n"
                                    "Use /attach_donation next"
    },
    'ua': {
        request_screenshot_message_id: "Дякуємо за твій донат! Давай зробимо швидке підтвердження, перш ніж ти "
                                       "зможеш відстежувати оновлення щодо свого внеску. Будь ласка, "
                                       "надішли скриншот свого платежу",
        file_too_large_message_id: "Файл слишком большой (max 10 MB)",
        invalid_email_message_id: "Недійсний формат електронної пошти",
        request_contacts_message_id: "Будь ласка, повідом нам адресу своєї електронної пошти, якщо бажаєш отримати "
                                     "підтвердження щодо того, на що буде витрачено твій донат, та побачити фотодоказ"
                                     " цього",
        no_need_for_confirmation_message_id: "Я не бажаю отримувати підтвердження",
        thanks_for_contacts_message_id: "Дякую! Ти можеш перевірити статус свого донату используя /donation_status",

        photo_not_attached_message_id: "Фото не додається",
        request_a_new_donation_message_id: "Якщо ти вже зробив донат з нами, обери /attach_donation\n"
                                           "Якщо ти бажаєш зробити донат, обери /new_donation",

        donation_status_message_id: "Подивитися статус мого донату",
        about_campaign_message_id: "Про кампанію",
        make_a_new_donation_message_id: "Зробити новий донат",

        you_did_not_upload_confirmation_message_id: "Ви не завантажили підтвердження",
        you_did_not_share_a_contact_message_id: "Ви не поділилися контактом",

        donation_status_first_day_message_id: "Твій донат підтверджено та буде передано нашим захисникам",
        donation_status_after_24h_message_id: "Твій донат перераховано нашим захисникам, запит уже виконується",
        donation_status_after_1week_message_id: "Твій донат наблизив нас на крок ближче до перемоги. Через деякий час "
                                                "ми надішлемо фотодоказ на твою електронну пошту. Дякуємо за твій "
                                                "внесок!",

        campaign_message_id: "Campaign link here",

        type_start_to_start_message_id: "Натисніть /start щоб почати",

        thanks_1_message_id: "Вітаємо! Ти щойно підстрелив орка! Дякуємо за твій донат",
        thanks_2_message_id: "Дякуємо за інвестицію у мирне майбутнє України! Твої відсотки у вигляді дерусифікованих "
                             "міст надійдуть зовсім скоро",
        thanks_3_message_id: "Вау, так ти мочеш російську техніку не лише в ЄБайрактар! Дякуємо за донат!",

        quick_payment_message_id: "Швидкий донат",
        payment_details_message_id: "Реквізити для оплати\n"
                                    "\n"
                                    "Банківська картка: {bank-card}\n"
                                    "IBAN: {bank-iban}\n"
                                    "\n"
                                    "Используйте /attach_donation далее"
    }
}

thanks_images = {
    thanks_1_message_id: "https://donnation-tracker-bot-upploads.s3.eu-central-1.amazonaws.com/thanks_1_message_id.jpg",
    thanks_2_message_id: "https://donnation-tracker-bot-upploads.s3.eu-central-1.amazonaws.com/thanks_2_message_id.jpg",
    thanks_3_message_id: "https://donnation-tracker-bot-upploads.s3.eu-central-1.amazonaws.com/thanks_3_message_id.jpg",
}


def localize(session: Session, message_id: str) -> str:
    language = 'eng' if session.language is None else session.language
    
    if message_id not in _messages[language]:
        raise Exception("Invalid message id")

    message = _messages[language][message_id]
    return message


def localize_random_thank_you(session: Session) -> Tuple[str, str]:
    message_id = random.choice([thanks_1_message_id, thanks_2_message_id, thanks_3_message_id])
    message_text = localize(session, message_id)
    image_url = thanks_images[message_id]
    return message_text, image_url
