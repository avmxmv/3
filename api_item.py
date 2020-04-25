from flask import abort, jsonify
from flask_restful import reqparse, abort, Resource

from data import db_session, items


def abort_if_item_not_found(item_id):
    session = db_session.create_session()
    item = session.query(items.Items).get(item_id)
    if not item:
        abort(404, message=f"Item {item_id} not found")


class ItemResource(Resource):
    def get(self, item_id):
        abort_if_item_not_found(item_id)
        session = db_session.create_session()
        item = session.query(items.Items).get(item_id)
        return jsonify({'item': item.to_dict()})

    def delete(self, item_id):
        abort_if_item_not_found(item_id)
        session = db_session.create_session()
        item = session.query(items.Items).get(item_id)
        session.delete(item)
        session.commit()
        return jsonify({'success': 'OK'})


parser = reqparse.RequestParser()
parser.add_argument('id', required=True)
parser.add_argument('title', required=True)
parser.add_argument('content', required=True)
parser.add_argument('price', required=True)
parser.add_argument('maxspeed', required=True)
parser.add_argument('boost', required=True)
parser.add_argument('power', required=True)
parser.add_argument('powerdensity', required=True)
parser.add_argument('size', required=True)
parser.add_argument('weight', required=True)


class ItemListResource(Resource):
    def get(self):
        session = db_session.create_session()
        item = session.query(items.Items).all()
        return jsonify({'item': [item_s.to_dict(
            only=('title', 'content')) for item_s in item]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        item = items.Items()
        item.id = args['id']
        item.title = args['title']
        item.content = args['content']
        item.price = args['price']
        item.maxspeed = args['maxspeed']
        item.boost = args['boost']
        item.power = args['power']
        item.powerdensity = args['powerdensity']
        item.size = args['size']
        item.weight = args['weight']
        session.add(item)
        session.commit()
        return jsonify({'success': 'OK'})
