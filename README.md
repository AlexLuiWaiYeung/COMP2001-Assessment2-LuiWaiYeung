# COMP2001 CW2: TrailService API

## Overview
A RESTful microservice for managing hiking trails, built with Flask and SQL Server.

## Features
- CRUD operations for trails
- Authentication via university API
- SQL Server database with CW2 schema
- RESTful API design

## Setup
1. Clone repository
2. Install dependencies: `pip install -r requirements.txt`
3. Configure `.env` file
4. Run: `python app.py`

## API Endpoints
- `GET /api/trails` - Get all trails
- `GET /api/trails/<id>` - Get specific trail
- `POST /api/trails` - Create trail (requires auth)
- `PUT /api/trails/<id>` - Update trail (requires auth)
- `DELETE /api/trails/<id>` - Delete trail (requires auth)

## Database Schema
- CW2.Trail: Trail information
- CW2.Location: Location data
- CW2.User: User accounts
- CW2.Sight: Points of interest

## Deployment
- Hosted at: `http://web.socem.plymouth.ac.uk/COMP2001/AlexLuiWaiYeung/`
- Database: `DIST-6-505.uopnet.plymouth.ac.uk`
