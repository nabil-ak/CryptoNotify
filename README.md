<img src="icon.png" alt="icon" width="256" hight="256"/>
# CryptoNotify

Discord Bot who notify you every hour with the newest Crypto prices.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirement frameworks.

```bash
pip install -r requirements.txt
```
## Settings
1. Change the ```channelID``` and the ```token```
2. Rename ```settings.example.json``` to ```settings.json```.
3. Add Cryptocurrencies to your ```Wallet``` and ```LastPrice``` (Ignore the price. The bot sets the price itself)

**Be aware just use Cryptocurrencies from [Coinbase](https://www.coinbase.com/price)**

```json
{
    "channelID": 92349347234436,
    "token": "uwertgwreugt23402340",
    "wallet": {
        "BTC": 0.00683409,
        "ETH": 0.02297584
    },
    "LastPrice": {
        "BTC": 31657.49,
        "ETH": 2284.24
    }
}
```
## Usage
Just run ```CryptoNotify.py```

## License
[MIT](https://choosealicense.com/licenses/mit/)