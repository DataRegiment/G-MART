import duckdb
import streamlit as st
from duckdb_utils import connect_duckdb, create_tables
import boto3
import json
import os
from datetime import datetime

def record_purchase_event(item, quantity, mobile_number, total_amount, delivery_location, payment_option):
    try:
        # Get DuckDB connection
        conn = connect_duckdb()
        
        # Record purchase in DuckDB
        conn.execute("""
            INSERT INTO purchase_events 
            (item_name, quantity, mobile_number, total_amount, delivery_location, 
             payment_option, purchase_timestamp, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (item, quantity, str(mobile_number), total_amount, delivery_location, 
              payment_option, datetime.now(), 'COMPLETED'))
        
        # Get the inserted record
        result = conn.execute("""
            SELECT * FROM purchase_events 
            WHERE mobile_number = ? 
            ORDER BY purchase_timestamp DESC LIMIT 1
        """, [str(mobile_number)]).fetchone()
        
        # Create event data for S3
        event_data = {
            "event_id": result[0],
            "item_name": item,
            "quantity": quantity,
            "mobile_number": str(mobile_number),
            "total_amount": float(total_amount),
            "delivery_location": delivery_location,
            "payment_option": payment_option,
            "purchase_timestamp": str(result[7]),
            "status": "COMPLETED"
        }

        
        # Send to S3
        send_to_s3(event_data)
        
        return True, "Purchase event recorded successfully"
        
    except Exception as e:
        return False, f"Error recording purchase: {str(e)}"

def send_to_s3(event_data):
    try:
        # Initialize S3 client
        s3_client = boto3.client('s3',
            aws_access_key_id=st.secrets['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=st.secrets['AWS_SECRET_ACCESS_KEY'],
            region_name=st.secrets['AWS_REGION']
        )
        
        # Create unique key for the event
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        event_key = f"purchase-events/{timestamp}_{event_data['event_id']}.json"
        
        # Upload to S3
        s3_client.put_object(
            Bucket=st.secrets['S3_BUCKET_NAME'],
            Key="events/"+event_key,
            Body=json.dumps(event_data),
            ContentType='application/json'
        )
        
    except Exception as e:
        print(f"Error sending to S3: {str(e)}")
        raise 