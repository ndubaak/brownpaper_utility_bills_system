from flask import Flask, request, redirect, url_for, session, flash, render_template
from models import storage
from datetime import datetime
from models.user import User
from models.utility import Utility
from models.customer import Customer
from models.payment import Payment
from models.payment_history import PaymentHistory
from werkzeug.security import check_password_hash

#app.secret_key = 'your_secret_key'  # Required for session handling
app = Flask(__name__)
app.secret_key = 'r1ac,dFF123'

app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        print(f"Login attempt with email: {email}")

        # Correct way to query user by email
        try:
            user = storage.query(User).filter_by(email=email).first()
        except Exception as e:
            print(f"Error querying user: {e}")
            flash('Database error occurred', 'error')
            return redirect(url_for('login'))
        
        if user is None:
            print("User not found")
            flash('Invalid email or password', 'error')
            return redirect(url_for('login'))

        # Check password
        if not user.check_password(password):
            print("Password mismatch")
            flash('Invalid email or password', 'error')
            return redirect(url_for('login'))

        # User authenticated successfully
        session['loggedin'] = True
        session['user_id'] = user.id
        flash('Login successful', 'success')
        return redirect(url_for('dashboard'))

    return render_template('homepage.html')


@app.route('/')
@app.route('/register', methods=['Get', 'Post'])
def register():
    if request.method == 'POST':
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')
        phone = request.form.get('phone')
        address = request.form.get('address')

        if not fullname or not email or not password or not confirm_password or not phone or not address:
            flash('Please fill out all fields.')
            return redirect(url_for('register'))

        if password != confirm_password:
            flash('Passwords do not match!')
            return redirect(url_for('register'))

        # Check if the email or username already exists
        existing_user = storage.all(User).get(f"User.{email}")  # Check by email
        if existing_user:
            flash('Email already registered. Please log in or use a different email.')
            return redirect(url_for('register'))

        # Create new User and Customer objects
        new_user = User( 
            username=fullname, # Assuming email as username
            email=email,
            password=User.hash_password(User, password)
        )
        new_customer = Customer(
            fullname=fullname,
            phone_number=phone,
            address=address,
            user_id=new_user.id  # Linking the customer to the user
        )

        try:
            # Save to database
            storage.new(new_user)
            storage.new(new_customer)
            storage.save()
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f"An error occurred during registration: {str(e)}")
            return redirect(url_for('register'))
    
    return render_template('register.html')




@app.route('/dashboard')
def dashboard():
    # Safely get user_id from session
    user_id = session.get('user_id')  
    if not user_id:
        flash('Please log in to access the dashboard.')
        return redirect(url_for('login'))

    # Query the customer using the user_id
    customer = storage.query(Customer).filter_by(user_id=user_id).first()
    # Log customer ID
    app.logger.info(f"Customer ID: {customer.id}")
    
    # Query all utilities and payment history
    utilities = storage.all(Utility)

    # Fetch payment histories for the current customer's payments
    payment_histories = (
        storage.query(PaymentHistory)
        .join(Payment)
        .filter(Payment.customer_id == customer.id)
        .all()
    )
    
    # Safely get user information from session
    return render_template(
        'dashboard.html',
        customer=customer,
        user=session.get('user'),  # Safely retrieve user info if present
        utilities=utilities,
        payment_histories=payment_histories  # Pass the payment histories to the template
    )


@app.route('/make_payment', methods=['GET', 'POST'])
def make_payment():
    if request.method == 'POST':    
        # Get utility data from form, use a default if company_name is not provided
        company_name = request.form.get('company_name') or 'Default Company Name'
        service_type = request.form.get('service_type')
        rate_per_unit = float(request.form.get('rate_per_unit'))
        customer_id = request.form.get('customer_id')
        amount = float(request.form.get('amount'))

        # Retrieve the customer by ID
        customer = storage.query(Customer).filter_by(id=customer_id).first()

        if not customer:
            flash("Customer not found!", "danger")
            return redirect(url_for('dashboard'))

        # Check if the utility already exists for the customer
        utility = storage.query(Utility).filter_by(
            company_name=company_name, 
            service_type=service_type, 
            customer_id=customer.id
        ).first()

        if not utility:
            # If the utility doesn't exist, create a new one
            utility = Utility(
                company_name=company_name,
                service_type=service_type,
                rate_per_unit=rate_per_unit,
                customer=customer
            )
            storage.new(utility)
            storage.save()

        # Create a new Payment entry
        payment = Payment(
            amount_paid=amount,
            payment_date=datetime.now(),
            payment_method='Credit Card',  # Can be dynamic
            utility=utility,  # Link payment to the utility
            customer=customer  # Link payment to the customer
        )

        # Save the payment to the database
        try:
            storage.new(payment)
            storage.save()  # Commit the payment to the database
            flash('Payment successful!', 'success')
        except Exception as e:
            storage.rollback()
            flash(f"Payment failed: {str(e)}", 'danger')

        return redirect(url_for('dashboard'))
    

@app.route('/update_profile', methods=['POST'])
def update_profile():
    if request.method == 'POST':
        user_id = session.get('user_id')  # Retrieve user_id from session
        customer = storage.query(Customer).filter_by(user_id=user_id).first()

        if not customer:
            flash('Customer not found.', 'danger')
            return redirect(url_for('dashboard'))

        # Update customer profile
        customer.fullname = request.form.get('fullname')
        customer.phone_number = request.form.get('phone')
        customer.email = request.form.get('email')

        try:
            storage.save()  # Save changes to the database
            flash('Profile updated successfully!', 'success')
        except Exception as e:
            storage.rollback()  # Rollback in case of an error
            print(f"Error updating profile: {str(e)}")  # Print error for debugging
            flash(f"Profile update failed: {str(e)}", 'danger')

        return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


# Close the session when the app context ends
#@app.teardown_appcontext
#def close_storage(exception=None):
   # storage.close()

if __name__ == '__main__':
    
    app.run(debug=True)