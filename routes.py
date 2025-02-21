from app import app, db
from flask import request, jsonify
from models import Friend

# Get all friends
@app.route('/api/friends', methods=['GET'])
def get_friends():
    friends = Friend.query.all()
    result = [friend.to_json() for friend in friends]
    return jsonify(result), 200


# Create a new friend
@app.route('/api/friends', methods=['POST'])
def create_friend():
    try:
        data = request.get_json()
        
        # Let's handle cases where user fails to input all the information
        required_fields = ["name", "role", "description", "gender"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        name = data.get('name')
        role = data.get('role')
        description = data.get('description')
        gender = data.get('gender')
       
       
        #    Fetch avatar image as per gender
        if gender == 'male':
            img_url = f"https://avatar.iran.liara.run/public/boy?username={name}"
        elif gender == 'female':
            img_url = f"https://avatar.iran.liara.run/public/girl?username={name}"
        else:
            img_url = None
        
        new_friend = Friend(name=name, role=role, description=description, gender=gender, img_url=img_url)
    
        db.session.add(new_friend)
        db.session.commit()
    
        return jsonify({"msg":"Friend added successfully"}), 201    
        # return jsonify(new_friend.to_json()), 201
        
    except Exception as e:
        # rollback if something went wrong
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
# Delete a friend
@app.route('/api/friends/<int:id>', methods=['DELETE'])
def delete_friend(id):
    try:
        friend = Friend.query.get(id)
        if not friend:
            return jsonify({"error": "Friend not found"}), 404
        
        db.session.delete(friend)
        db.session.commit()
    
        return jsonify({"msg":"Friend deleted successfully"}), 200
    
    except Exception as e:
        # rollback if something went wrong
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    

# Update a friend
@app.route('/api/friends/<int:id>', methods=['PATCH'])
def update_friend(id):
    try:
        friend = Friend.query.get(id)
        if not friend:
            return jsonify({"error": "Friend not found"}), 404
        
        data = request.get_json()
        
        # So here we update the fields, but also make sure if no updates are made we set a default value.
        friend.name = data.get('name', friend.name)
        friend.role = data.get('role', friend.role)
        friend.description = data.get('description', friend.description)
        friend.gender = data.get('gender', friend.gender)
        
        db.session.commit()
        return jsonify(friend.to_json()), 200
    
    except Exception as e:
        # rollback if something went wrong
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

