from flask_restful import Resource, request
from models.item import ItemModel
from models.entity import EntityModel
from schemas.item import ItemSchema

from pprint import pprint

item_schema = ItemSchema()
item_list_schema = ItemSchema(many=True)


class Item(Resource):
    @classmethod
    def get(cls, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item_schema.dump(item), 200
        return {'message': 'Item not found.'}, 404

    @classmethod
    def post(cls, name):
        #if ItemModel.find_by_name(name):
        #    return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = request.get_json()
        data['name'] = name
        item = item_schema.load(data)

        try:
            item.save_to_db()
        except:
            return {'message': 'An error occurre inserting the item.'}, 500

        return item_schema.dump(item), 201

    @classmethod
    def delete(cls, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': 'Item deleted.'}, 200

    @classmethod
    def put(cls, name):
        data = request.get_json()
        item = ItemModel.find_by_name(name)

        if item is None:
            data['name'] = name
            item = item_schema.load(data)
        else:
            item.sale = data['sale']
            item.buy = data['buy']

        item.save_to_db()
        return item_schema.dump(item)


class ItemList(Resource):
    @classmethod
    def get(cls):
        return {'items': item_list_schema.dump(ItemModel.find_all())}

    @classmethod
    def post(cls):
        data = request.get_json()

        for item_data in data:
            entity_name = item_data['entity_name']
            entity_address = item_data['entity_address']
            entity_phone = item_data['entity_phone']

            entity_id = EntityModel.find_id_by_name(entity_name)
            if not entity_id:
                entity = EntityModel(name=entity_name, address=entity_address, phone=entity_phone)
                try:
                    entity.save_to_db()
                except:
                    return {'message': 'An error occurred while creating the store.'}, 500
                entity_id = entity.id
            item['entity_id'] = entity_id
            item = item_schema.load(item_data)

            try:
                item.save_to_db()
            except:
                return {'message': 'An error occurre inserting the item.'}, 500

        return {'message': 'Data posted.'}, 201