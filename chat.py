from influxdb_client import InfluxDBClient
from influxdb_client.client.query_api import QueryApi
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext

# Configuration for InfluxDB
INFLUXDB_URL = 'http://localhost:8086/'
INFLUXDB_TOKEN = 'M2CerYISdJb1ddkYGtNo9m110Vfp8k90xoM0kf67BRcTGNlpcap6iv7yffG_MNOwofEF-8WiO-Hv7AvEO_Hc8g=='
INFLUXDB_ORG = 'BEIA'
INFLUXDB_BUCKET = 'dataBase'

# Configuration for Telegram Bot
TELEGRAM_TOKEN = '7321571357:AAElUNBvCu0gkOZFzuJjnL5qA0ssh1CW-SE'

# Initialize the InfluxDB client
client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN)
query_api = client.query_api()

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Hi! Use /temperature to get temperature values or /glucose to get glucose_level.')

async def temperature(update: Update, context: CallbackContext) -> None:
    query_text = f'''
    from(bucket: "{INFLUXDB_BUCKET}")
      |> range(start: -5m)
      |> filter(fn: (r) => r._measurement == "health")
      |> filter(fn: (r) => r._field == "temperature")
    '''
    try:
        tables = query_api.query(org=INFLUXDB_ORG, query=query_text)
        health_data = {}
        
        for table in tables:
            for record in table.records:
                time = record.get_time()
                sensor_id = record.get_field()
                
                if time not in health_data:
                    health_data[time] = {}
                health_data[time][sensor_id] = record.get_value()
        
        results = ""
        for time, data in health_data.items():
            formated_time = time.strftime('%Y-%m-%d %H:%M:%S')
            print(data)
            results = f'Time: {formated_time}, Temperature: {data.get("temperature")}'
        
        if results:
            await update.message.reply_text(results)
        else:
            await update.message.reply_text('No temperature values found.')
            
    except Exception as e:
        await update.message.reply_text(f'Error executing query: {str(e)}')


async def glucose(update: Update, context: CallbackContext) -> None:
    query_text = f'''
    from(bucket: "{INFLUXDB_BUCKET}")
      |> range(start: -5m)
      |> filter(fn: (r) => r._measurement == "health")
      |> filter(fn: (r) => r._field == "glucose_level")
    '''
    try:
        tables = query_api.query(org=INFLUXDB_ORG, query=query_text)
        health_data = {}
        
        for table in tables:
            for record in table.records:
                time = record.get_time()
                sensor_id = record.get_field()
                
                if time not in health_data:
                    health_data[time] = {}
                health_data[time][sensor_id] = record.get_value()
        
        results = ""
        for time, data in health_data.items():
            formated_time = time.strftime('%Y-%m-%d %H:%M:%S')
            print(data)
            results = f'Time: {formated_time}, Glucose_level: {data.get("glucose_level")}'
        
        if results:
            await update.message.reply_text(results)
        else:
            await update.message.reply_text('No glucose_level values found.')
            
    except Exception as e:
        await update.message.reply_text(f'Error executing query: {str(e)}')


def main() -> None:
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("temperature", temperature))
    application.add_handler(CommandHandler("glucose", glucose))

    application.run_polling()

if __name__ == '__main__':
    main()
