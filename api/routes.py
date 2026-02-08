from flask import Blueprint, request, jsonify
from database.connection import get_db
import pyodbc

# Create blueprint
trails_bp = Blueprint('trails', __name__, url_prefix='/api')


@trails_bp.route('/trails', methods=['GET'])
def get_all_trails():
    """
    GET /api/trails - Get all trails from REAL database
    """
    try:
        conn = get_db()
        if conn is None:
            return jsonify({
                'success': False,
                'error': 'Database connection not available'
            }), 500

        cursor = conn.cursor()

        # Query CW2 schema (adjust based on your actual schema)
        cursor.execute("""
                       SELECT TrailID,
                              TrailName,
                              Rating,
                              Difficulty,
                              Length,
                              ElevationGain,
                              EstimatedTime,
                              Loop,
                              Description,
                              LocationID,
                              OwnerID
                       FROM CW2.Trail
                       ORDER BY TrailID
                       """)

        rows = cursor.fetchall()
        trails = []
        columns = [column[0] for column in cursor.description]

        for row in rows:
            trail = dict(zip(columns, row))
            # Convert BIT to boolean
            if 'Loop' in trail:
                trail['Loop'] = bool(trail['Loop'])
            trails.append(trail)

        cursor.close()

        return jsonify({
            'success': True,
            'count': len(trails),
            'trails': trails,
            'schema': 'CW2',
            'database': 'live'
        }), 200

    except pyodbc.Error as e:
        print(f"Database error: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'note': 'Database query failed'
        }), 500
    except Exception as e:
        print(f"General error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@trails_bp.route('/test-db', methods=['GET'])
def test_db():
    """
    Simple endpoint to test database connection
    """
    try:
        conn = get_db()
        if conn is None:
            return jsonify({'status': 'Database connection failed'}), 500

        cursor = conn.cursor()
        cursor.execute("SELECT @@VERSION")
        version = cursor.fetchone()[0]
        cursor.close()

        return jsonify({
            'status': 'Database connected',
            'version': version[:100]
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'Database error',
            'error': str(e)
        }), 500


# ========== CREATE TRAIL (POST) ==========
@trails_bp.route('/trails', methods=['POST'])
def create_trail():
    """POST /api/trails - Create new trail"""
    try:
        data = request.get_json()

        # Validate required fields
        required = ['TrailName', 'Difficulty', 'Length', 'LocationID']
        for field in required:
            if field not in data:
                return jsonify({'error': f'Missing {field}'}), 400

        conn = get_db()
        cursor = conn.cursor()

        # Insert into database
        cursor.execute("""
                       INSERT INTO CW2.Trail
                       (TrailName, Rating, Difficulty, Length, ElevationGain,
                        EstimatedTime, Loop, Description, LocationID, OwnerID)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                       """, (
                           data['TrailName'],
                           data.get('Rating'),
                           data['Difficulty'],
                           data['Length'],
                           data.get('ElevationGain', 0),
                           data.get('EstimatedTime', '1 hour'),
                           data.get('Loop', False),
                           data.get('Description', ''),
                           data['LocationID'],
                           data.get('OwnerID', 1)  # Default to first user
                       ))

        conn.commit()
        new_id = cursor.execute("SELECT SCOPE_IDENTITY()").fetchone()[0]
        cursor.close()

        return jsonify({
            'success': True,
            'message': 'Trail created',
            'trail_id': new_id
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ========== UPDATE TRAIL (PUT) ==========
@trails_bp.route('/trails/<int:trail_id>', methods=['PUT'])
def update_trail(trail_id):
    """PUT /api/trails/<id> - Update trail"""
    try:
        data = request.get_json()

        conn = get_db()
        cursor = conn.cursor()

        # Build dynamic UPDATE query
        updates = []
        params = []

        fields = {
            'TrailName': data.get('TrailName'),
            'Rating': data.get('Rating'),
            'Difficulty': data.get('Difficulty'),
            'Length': data.get('Length'),
            'ElevationGain': data.get('ElevationGain'),
            'EstimatedTime': data.get('EstimatedTime'),
            'Loop': data.get('Loop'),
            'Description': data.get('Description'),
            'LocationID': data.get('LocationID')
        }

        for field, value in fields.items():
            if value is not None:
                updates.append(f"{field} = ?")
                params.append(value)

        if not updates:
            return jsonify({'error': 'No fields to update'}), 400

        params.append(trail_id)  # For WHERE clause

        query = f"UPDATE CW2.Trail SET {', '.join(updates)} WHERE TrailID = ?"
        cursor.execute(query, params)
        conn.commit()

        affected = cursor.rowcount
        cursor.close()

        if affected == 0:
            return jsonify({'error': 'Trail not found'}), 404

        return jsonify({
            'success': True,
            'message': f'Trail {trail_id} updated'
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ========== DELETE TRAIL ==========
@trails_bp.route('/trails/<int:trail_id>', methods=['DELETE'])
def delete_trail(trail_id):
    """DELETE /api/trails/<id> - Delete trail"""
    try:
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM CW2.Trail WHERE TrailID = ?", (trail_id,))
        conn.commit()

        affected = cursor.rowcount
        cursor.close()

        if affected == 0:
            return jsonify({'error': 'Trail not found'}), 404

        return jsonify({
            'success': True,
            'message': f'Trail {trail_id} deleted'
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500