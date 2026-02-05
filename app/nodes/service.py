#app/nodes/service.py
import secrets
from datetime import datetime
from app.extensions import db
from .models import Node

def register_node(org_id,data):
   
    generated_key=secrets.token_hex(32)
   
    new_node=Node(
        name=data.get('name'),
        node_type=data.get('node_type', 'sensor'),
        organization_id=org_id,
        api_key=generated_key

    )
    
    try:
        db.session.add(new_node)
        db.session.commit()
        new_node.api_key=generated_key
        return new_node
    except Exception as e:
        db.session.rollback()
        raise ValueError("Error creating node: " + str(e))
    
    

def get_nodes_by_organization(org_id):
    nodes=Node.query.filter_by(organization_id=org_id).all()
    return nodes

def get_nodes_by_role(role,org_id):
    if role == 'admin':
        nodes=Node.query.all()
    else:
        nodes=Node.query.filter_by(organization_id=org_id).all()
    return nodes

def get_node_by_id(node_id,org_id,role):

    if role == 'admin':
        node= Node.query.get(node_id)
    else:
        node=Node.query.filter_by(id=node_id, organization_id=org_id).first()
    return node

def process_heartbeat(node_id):
    node=Node.query.get(node_id)
    if not node:
        raise ValueError("Node not found")
    
    node.last_seen=datetime.utcnow()
    node.status='active'

    try:
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        return False
    
   

def delete_node(node_id,org_id):
    node=Node.query.filter_by(id=node_id, organization_id=org_id).first()
    if not node:
        raise ValueError("Node not found")
    
    try:
        db.session.delete(node)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise ValueError("Error deleting node: " + str(e))
    
    return {
        "message": f"Node {node.name} deleted successfully",
        
    }, 200

