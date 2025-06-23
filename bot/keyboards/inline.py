from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.localization import t
from bot.database.methods import get_category_parent


def main_menu(role: int, channel: str = None, helper: str = None, lang: str = 'en') -> InlineKeyboardMarkup:
    inline_keyboard = [
        [InlineKeyboardButton(t(lang, 'shop'), callback_data='shop')],
        [
            InlineKeyboardButton(t(lang, 'profile'), callback_data='profile'),
            InlineKeyboardButton(t(lang, 'top_up'), callback_data='replenish_balance')
        ]
    ]
    row = []
    if channel:
        row.append(InlineKeyboardButton(t(lang, 'channel'), url=f"https://t.me/{channel}"))
    if helper:
        row.append(InlineKeyboardButton(t(lang, 'support'), url=f"https://t.me/{helper.lstrip('@')}"))
    if row:
        inline_keyboard.append(row)
    inline_keyboard.append([InlineKeyboardButton(t(lang, 'language'), callback_data='change_language')])
    if role > 1:
        inline_keyboard.append([InlineKeyboardButton(t(lang, 'admin_panel'), callback_data='console')])

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def categories_list(list_items: list[str], current_index: int, max_index: int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    page_items = list_items[current_index * 10: (current_index + 1) * 10]
    for name in page_items:
        markup.add(InlineKeyboardButton(text=name, callback_data=f'category_{name}'))
    if max_index > 0:
        buttons = [
            InlineKeyboardButton(text='◀️', callback_data=f'categories-page_{current_index - 1}'),
            InlineKeyboardButton(text=f'{current_index + 1}/{max_index + 1}', callback_data='dummy_button'),
            InlineKeyboardButton(text='▶️', callback_data=f'categories-page_{current_index + 1}')
        ]
        markup.row(*buttons)
    markup.add(InlineKeyboardButton('🔙 Back to menu', callback_data='back_to_menu'))
    return markup


def goods_list(list_items: list[str], category_name: str, current_index: int, max_index: int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    page_items = list_items[current_index * 10: (current_index + 1) * 10]
    for name in page_items:
        markup.add(InlineKeyboardButton(text=name, callback_data=f'item_{name}'))
    if max_index > 0:
        buttons = [
            InlineKeyboardButton(text='◀️', callback_data=f'goods-page_{category_name}_{current_index - 1}'),
            InlineKeyboardButton(text=f'{current_index + 1}/{max_index + 1}', callback_data='dummy_button'),
            InlineKeyboardButton(text='▶️', callback_data=f'goods-page_{category_name}_{current_index + 1}')
        ]
        markup.row(*buttons)
    markup.add(InlineKeyboardButton('🔙 Go back', callback_data='shop'))
    return markup


def subcategories_list(list_items: list[str], parent: str, current_index: int, max_index: int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    page_items = list_items[current_index * 10: (current_index + 1) * 10]
    for name in page_items:
        markup.add(InlineKeyboardButton(text=name, callback_data=f'category_{name}'))
    if max_index > 0:
        buttons = [
            InlineKeyboardButton(text='◀️', callback_data=f'subcategories-page_{parent}_{current_index - 1}'),
            InlineKeyboardButton(text=f'{current_index + 1}/{max_index + 1}', callback_data='dummy_button'),
            InlineKeyboardButton(text='▶️', callback_data=f'subcategories-page_{parent}_{current_index + 1}')
        ]
        markup.row(*buttons)
    back_parent = get_category_parent(parent)
    back_data = 'shop' if back_parent is None else f'category_{back_parent}'
    markup.add(InlineKeyboardButton('🔙 Go back', callback_data=back_data))
    return markup


def user_items_list(list_items: list, data: str, back_data: str, pre_back: str, current_index: int, max_index: int)\
        -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    page_items = list_items[current_index * 10: (current_index + 1) * 10]
    for item in page_items:
        markup.add(InlineKeyboardButton(text=item.item_name, callback_data=f'bought-item:{item.id}:{pre_back}'))
    if max_index > 0:
        buttons = [
            InlineKeyboardButton(text='◀️', callback_data=f'bought-goods-page_{current_index - 1}_{data}'),
            InlineKeyboardButton(text=f'{current_index + 1}/{max_index + 1}', callback_data='dummy_button'),
            InlineKeyboardButton(text='▶️', callback_data=f'bought-goods-page_{current_index + 1}_{data}')
        ]
        markup.row(*buttons)
    markup.add(InlineKeyboardButton('🔙 Go back', callback_data=back_data))
    return markup


def item_info(item_name: str, category_name: str) -> InlineKeyboardMarkup:
    inline_keyboard = [
        [InlineKeyboardButton('💰 Buy', callback_data=f'buy_{item_name}')],
        [InlineKeyboardButton('🔙 Go back', callback_data=f'category_{category_name}')
         ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def profile(referral_percent: int, user_items: int = 0) -> InlineKeyboardMarkup:
    inline_keyboard = [
        [InlineKeyboardButton('💸 Top up balance', callback_data='replenish_balance')
         ]
    ]
    if referral_percent != 0:
        inline_keyboard.append([InlineKeyboardButton('🎲 Referral system', callback_data='referral_system')])
    if user_items != 0:
        inline_keyboard.append([InlineKeyboardButton('🎁 Purchased items', callback_data='bought_items')])
    inline_keyboard.append([InlineKeyboardButton('🔙 Back to menu', callback_data='back_to_menu')])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def rules() -> InlineKeyboardMarkup:
    inline_keyboard = [
        [InlineKeyboardButton('🔙 Back to menu', callback_data='back_to_menu')
         ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def console() -> InlineKeyboardMarkup:
    inline_keyboard = [
        [InlineKeyboardButton('🏪 Shop management', callback_data='shop_management')
         ],
        [InlineKeyboardButton('👥 User management', callback_data='user_management')
         ],
        [InlineKeyboardButton('📢 Broadcast', callback_data='send_message')
         ],
        [InlineKeyboardButton('🔙 Back to menu', callback_data='back_to_menu')
         ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def user_management(admin_role: int, user_role: int, admin_manage: int, items: int, user_id: int) \
        -> InlineKeyboardMarkup:
    inline_keyboard = [
        [
            InlineKeyboardButton('💸 Top up balance User', callback_data=f'fill-user-balance_{user_id}')
        ]
    ]
    if items > 0:
        inline_keyboard.append([InlineKeyboardButton('🎁 Purchased items', callback_data=f'user-items_{user_id}')])
    if admin_role >= admin_manage and admin_role > user_role:
        if user_role == 1:
            inline_keyboard.append(
                [InlineKeyboardButton('⬆️ Assign admin', callback_data=f'set-admin_{user_id}')])
        else:
            inline_keyboard.append(
                [InlineKeyboardButton('⬇️ Remove admin', callback_data=f'remove-admin_{user_id}')])
    inline_keyboard.append([InlineKeyboardButton('🔙 Go back', callback_data='user_management')])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def user_manage_check(user_id: int) -> InlineKeyboardMarkup:
    inline_keyboard = [
        [InlineKeyboardButton('✅ Yes', callback_data=f'check-user_{user_id}')
         ],
        [InlineKeyboardButton('🔙 Go back', callback_data='user_management')
         ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def shop_management() -> InlineKeyboardMarkup:
    inline_keyboard = [
        [InlineKeyboardButton('Item management', callback_data='goods_management')
         ],
        [InlineKeyboardButton('Category management', callback_data='categories_management')
         ],
        [InlineKeyboardButton('Show logs', callback_data='show_logs')
         ],
        [InlineKeyboardButton('Statistics', callback_data='statistics')
         ],
        [InlineKeyboardButton('🔙 Go back', callback_data='console')
         ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def goods_management() -> InlineKeyboardMarkup:
    inline_keyboard = [
        [InlineKeyboardButton('add item', callback_data='item-management'),
         InlineKeyboardButton('update item', callback_data='update_item'),
         InlineKeyboardButton('delete item', callback_data='delete_item')
         ],
        [InlineKeyboardButton('Show purchased item info', callback_data='show_bought_item')
         ],
        [InlineKeyboardButton('🔙 Go back', callback_data='shop_management')
         ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def item_management() -> InlineKeyboardMarkup:
    inline_keyboard = [
        [InlineKeyboardButton('create item', callback_data='add_item'),
         InlineKeyboardButton('add to existing item', callback_data='update_item_amount'),
         ],
        [InlineKeyboardButton('🔙 Go back', callback_data='goods_management')
         ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def categories_management() -> InlineKeyboardMarkup:
    inline_keyboard = [
        [InlineKeyboardButton('add category', callback_data='add_category'),
         InlineKeyboardButton('add subcategory', callback_data='add_subcategory')],
        [InlineKeyboardButton('update category', callback_data='update_category'),
         InlineKeyboardButton('delete category', callback_data='delete_category')],
        [InlineKeyboardButton('🔙 Go back', callback_data='shop_management')
         ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def close() -> InlineKeyboardMarkup:
    inline_keyboard = [
        [InlineKeyboardButton('Hide', callback_data='close')
         ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def check_sub(channel_username: str) -> InlineKeyboardMarkup:
    inline_keyboard = [
        [InlineKeyboardButton('Subscribe', url=f'https://t.me/{channel_username}')
         ],
        [InlineKeyboardButton('Check', callback_data='sub_channel_done')
         ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def back(callback: str) -> InlineKeyboardMarkup:
    inline_keyboard = [
        [InlineKeyboardButton('🔙 Go back', callback_data=callback)
         ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def payment_menu(url: str, label: str) -> InlineKeyboardMarkup:
    inline_keyboard = [
        [InlineKeyboardButton('✅ Pay', url=url)
         ],
        [InlineKeyboardButton('🔄 Check payment', callback_data=f'check_{label}')
         ],
        [InlineKeyboardButton('🔙 Go back', callback_data='replenish_balance')
         ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def reset_config(key: str) -> InlineKeyboardMarkup:
    inline_keyboard = [
        [InlineKeyboardButton(f'Reset {key}', callback_data=f'reset_{key}')
         ],
        [InlineKeyboardButton('🔙 Go back', callback_data='settings')
         ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def question_buttons(question: str, back_data: str) -> InlineKeyboardMarkup:
    inline_keyboard = [
        [InlineKeyboardButton('✅ Yes', callback_data=f'{question}_yes'),
         InlineKeyboardButton('❌ No', callback_data=f'{question}_no')
         ],
        [InlineKeyboardButton('🔙 Go back', callback_data=back_data)
         ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
