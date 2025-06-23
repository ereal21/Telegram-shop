import os
from bot.database.models import Database, Goods, ItemValues, Categories, UnfinishedOperations


def delete_item(item_name: str) -> None:
    values = Database().session.query(ItemValues.value).filter(ItemValues.item_name == item_name).all()
    for val in values:
        if os.path.isfile(val[0]):
            os.remove(val[0])
    Database().session.query(Goods).filter(Goods.name == item_name).delete()
    Database().session.query(ItemValues).filter(ItemValues.item_name == item_name).delete()
    Database().session.commit()


def delete_only_items(item_name: str) -> None:
    values = Database().session.query(ItemValues.value).filter(ItemValues.item_name == item_name).all()
    for val in values:
        if os.path.isfile(val[0]):
            os.remove(val[0])
    Database().session.query(ItemValues).filter(ItemValues.item_name == item_name).delete()


def delete_category(category_name: str) -> None:
    goods = Database().session.query(Goods.name).filter(Goods.category_name == category_name).all()
    for item in goods:
        values = Database().session.query(ItemValues.value).filter(ItemValues.item_name == item.name).all()
        for val in values:
            if os.path.isfile(val[0]):
                os.remove(val[0])
        Database().session.query(ItemValues).filter(ItemValues.item_name == item.name).delete()
    Database().session.query(Goods).filter(Goods.category_name == category_name).delete()
    Database().session.query(Categories).filter(Categories.name == category_name).delete()
    Database().session.commit()


def finish_operation(operation_id: str) -> None:
    Database().session.query(UnfinishedOperations).filter(UnfinishedOperations.operation_id == operation_id).delete()
    Database().session.commit()


def buy_item(item_id: str, infinity: bool = False) -> None:
    if infinity is False:
        value = Database().session.query(ItemValues.value).filter(ItemValues.id == item_id).first()
        if value and os.path.isfile(value[0]):
            os.remove(value[0])
        Database().session.query(ItemValues).filter(ItemValues.id == item_id).delete()
        Database().session.commit()
    else:
        pass
