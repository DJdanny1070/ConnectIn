"""
Payment service for handling payments in Indian market
Supports UPI, Net Banking, Cards, and Wallets
This is a mock implementation - integrate with actual payment gateways in production
"""

import uuid
from datetime import datetime
import random

class PaymentService:
    """Service to handle payment processing for Indian market"""
    
    def __init__(self):
        # Supported payment methods in India
        self.payment_methods = {
            'upi': ['gpay', 'phonepe', 'paytm', 'bhim'],
            'netbanking': ['sbi', 'hdfc', 'icici', 'axis', 'kotak'],
            'card': ['visa', 'mastercard', 'rupay'],
            'wallet': ['paytm', 'phonepe', 'mobikwik', 'amazon_pay']
        }
        
        # Mock payment gateway fees (in percentage)
        self.gateway_fees = {
            'razorpay': 2.0,
            'paytm': 2.5,
            'phonepe': 1.99,
            'cashfree': 1.95,
            'instamojo': 2.0
        }
    
    def process_payment(self, payment) -> dict:
        """
        Process a payment transaction
        In production, this would integrate with actual payment gateways
        """
        try:
            # Generate transaction ID
            transaction_id = self._generate_transaction_id()
            payment.transaction_id = transaction_id
            
            # Select payment gateway (mock)
            gateway = self._select_gateway(payment.payment_method)
            payment.payment_gateway = gateway
            
            # Calculate fees
            fee_amount = self._calculate_fees(payment.amount, gateway)
            
            # Simulate payment processing
            success = self._simulate_payment_processing(payment)
            
            if success:
                payment.status = 'held'  # Hold payment in escrow
                payment.completed_at = datetime.utcnow()
                
                return {
                    'success': True,
                    'transaction_id': transaction_id,
                    'gateway': gateway,
                    'fee_amount': fee_amount,
                    'net_amount': payment.amount - fee_amount,
                    'status': 'held',
                    'message': 'Payment successful and held in escrow'
                }
            else:
                payment.status = 'failed'
                
                return {
                    'success': False,
                    'transaction_id': transaction_id,
                    'gateway': gateway,
                    'status': 'failed',
                    'message': 'Payment failed. Please try again.'
                }
        
        except Exception as e:
            payment.status = 'failed'
            return {
                'success': False,
                'error': str(e),
                'message': 'Payment processing error'
            }
    
    def release_payment_to_freelancer(self, payment) -> dict:
        """
        Release payment from escrow to freelancer
        """
        try:
            if payment.status != 'held':
                return {
                    'success': False,
                    'message': 'Payment is not in held status'
                }
            
            # In production, this would trigger actual fund transfer
            payment.status = 'completed'
            payment.released_at = datetime.utcnow()
            
            return {
                'success': True,
                'message': 'Payment released to freelancer',
                'released_amount': payment.amount,
                'released_at': payment.released_at.isoformat()
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Error releasing payment'
            }
    
    def refund_payment(self, payment) -> dict:
        """
        Process refund for a payment
        """
        try:
            if payment.status not in ['held', 'completed']:
                return {
                    'success': False,
                    'message': 'Payment cannot be refunded'
                }
            
            # Generate refund transaction ID
            refund_id = f"REFUND_{self._generate_transaction_id()}"
            
            payment.status = 'refunded'
            
            return {
                'success': True,
                'refund_id': refund_id,
                'refund_amount': payment.amount,
                'message': 'Refund processed successfully'
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Error processing refund'
            }
    
    def validate_payment_method(self, method: str, details: dict = None) -> bool:
        """
        Validate if payment method is supported and details are correct
        """
        method_lower = method.lower()
        
        if method_lower == 'upi':
            return self._validate_upi(details)
        elif method_lower == 'netbanking':
            return self._validate_netbanking(details)
        elif method_lower == 'card':
            return self._validate_card(details)
        elif method_lower == 'wallet':
            return self._validate_wallet(details)
        else:
            return False
    
    def get_supported_methods(self) -> dict:
        """
        Get all supported payment methods
        """
        return {
            'payment_methods': self.payment_methods,
            'recommended': {
                'upi': 'Fast and free instant payments',
                'netbanking': 'Direct bank transfers',
                'card': 'Credit/Debit cards accepted',
                'wallet': 'Digital wallet payments'
            }
        }
    
    def calculate_platform_fee(self, amount: float, user_type: str = 'freelancer') -> dict:
        """
        Calculate platform commission/fee
        """
        # Platform fees
        if user_type == 'freelancer':
            # Freelancer pays 10% platform fee
            fee_percentage = 10.0
        else:
            # Employer pays 5% platform fee
            fee_percentage = 5.0
        
        fee_amount = (amount * fee_percentage) / 100
        net_amount = amount - fee_amount
        
        return {
            'gross_amount': amount,
            'fee_percentage': fee_percentage,
            'fee_amount': fee_amount,
            'net_amount': net_amount
        }
    
    def _generate_transaction_id(self) -> str:
        """Generate unique transaction ID"""
        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        random_suffix = str(uuid.uuid4())[:8].upper()
        return f"TXN{timestamp}{random_suffix}"
    
    def _select_gateway(self, payment_method: str) -> str:
        """
        Select appropriate payment gateway based on method
        In production, this would consider gateway availability, fees, success rates
        """
        gateways = {
            'upi': 'razorpay',
            'netbanking': 'razorpay',
            'card': 'razorpay',
            'wallet': 'paytm'
        }
        
        return gateways.get(payment_method.lower(), 'razorpay')
    
    def _calculate_fees(self, amount: float, gateway: str) -> float:
        """Calculate gateway fees"""
        fee_percentage = self.gateway_fees.get(gateway, 2.0)
        return (amount * fee_percentage) / 100
    
    def _simulate_payment_processing(self, payment) -> bool:
        """
        Simulate payment processing
        In production, this would call actual payment gateway APIs
        """
        # Simulate 95% success rate
        return random.random() < 0.95
    
    def _validate_upi(self, details: dict) -> bool:
        """Validate UPI payment details"""
        if not details:
            return True  # Basic validation
        
        upi_id = details.get('upi_id', '')
        # Basic UPI ID format: username@bank
        return '@' in upi_id and len(upi_id) > 5
    
    def _validate_netbanking(self, details: dict) -> bool:
        """Validate net banking details"""
        if not details:
            return True
        
        bank = details.get('bank', '').lower()
        return bank in self.payment_methods.get('netbanking', [])
    
    def _validate_card(self, details: dict) -> bool:
        """Validate card details"""
        if not details:
            return True
        
        card_number = details.get('card_number', '')
        cvv = details.get('cvv', '')
        
        # Basic validation
        return len(card_number) >= 13 and len(cvv) == 3
    
    def _validate_wallet(self, details: dict) -> bool:
        """Validate wallet details"""
        if not details:
            return True
        
        wallet = details.get('wallet', '').lower()
        return wallet in self.payment_methods.get('wallet', [])
    
    def get_transaction_status(self, transaction_id: str) -> dict:
        """
        Get status of a transaction
        In production, this would query the payment gateway
        """
        # Mock implementation
        return {
            'transaction_id': transaction_id,
            'status': 'completed',
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def create_payout(self, freelancer_id: int, amount: float, 
                     account_details: dict) -> dict:
        """
        Create payout to freelancer's bank account
        """
        try:
            payout_id = f"PAYOUT_{self._generate_transaction_id()}"
            
            # In production, integrate with payout APIs
            # Razorpay Payouts, Cashfree Payouts, etc.
            
            return {
                'success': True,
                'payout_id': payout_id,
                'amount': amount,
                'status': 'processing',
                'estimated_time': '2-3 business days',
                'message': 'Payout initiated successfully'
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Error creating payout'
            }
