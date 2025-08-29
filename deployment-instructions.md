
# Biryani Club - Deployment Instructions

## Deploy to Render

1. **Create a new account on Render.com**
2. **Upload the biryani-club-deployment.zip file**
3. **Configure the deployment:**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn --bind 0.0.0.0:$PORT main:app`
   - Environment Variables:
     - `FLASK_ENV=production`
     - `SECRET_KEY=your-secret-key-here`

## Features Included
- ✅ Real-time order tracking with IST timezone
- ✅ Admin panel for order management
- ✅ Mobile-friendly responsive design
- ✅ UPI payment integration with QR codes
- ✅ Coupon system
- ✅ Guest checkout functionality
- ✅ Order status updates
- ✅ Beautiful UI with orange theme

## Default Login Credentials
- **Admin:** admin / admin123
- **Delivery:** delivery1 / delivery123

## File Structure
```
biryani-club/
├── app.py              # Flask application setup
├── main.py             # Application entry point
├── models.py           # Database models
├── routes.py           # Application routes
├── utils.py            # Utility functions
├── requirements.txt    # Python dependencies
├── Procfile           # Deployment configuration
├── render.yaml        # Render deployment config
├── static/            # CSS, JS, images
├── templates/         # HTML templates
└── reset_db.py        # Database initialization
```

## Post-Deployment Steps
1. Access your deployed app URL
2. Run database initialization (first time only)
3. Login with admin credentials to configure store settings
4. Add menu items through admin panel
5. Test order placement and tracking

Your application is now ready for production!
