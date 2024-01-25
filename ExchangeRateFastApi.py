from fastapi import FastAPI, Query
from typing import List
import currencyapicom

app = FastAPI()
client = currencyapicom.Client('cur_live_Ht7cwEfYvrVC1bbDJTvjhWEkVqwHW5d71kN5BK5k')


@app.get("/convert_currency/")
async def convert_currency(
        input_currency: str = Query(..., title="Input currency", description="Currency code for the input"),
        output_currencies: List[str] = Query(..., title="Output currencies",
                                             description="List of currency codes for the output", min_length=1),
        amount: float = Query(..., title="Amount", description="Amount to convert"),
        date: str = Query(..., title="Date", description="Conversion date in YYYY-MM-DD format")
):
    result = client.historical(date)

    converted_data = []
    for output_currency in output_currencies:
        conversion_rate = result['data'][output_currency]['value'] / result['data'][input_currency]['value']
        converted_amount = amount * conversion_rate
        converted_data.append({"currency": output_currency, "amount": round(converted_amount, 2)})

    return converted_data