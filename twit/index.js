var Twit = require('twit')

var T = new Twit({
    consumer_key:         'CCoafJyLpbGe9gTPkIL8ciEFK',
    consumer_secret:      'y9rMFlis3BjkoUoHfSg2fWaqNhYTHFkN6AtQTvZN0SBBNNR93O',
    access_token:         '1445107177945960458-9cP5yN036RQKeGIcyoEZKHMRP1C3dB',
    access_token_secret:  'rgNmxt8X7BDOBkACyqobsFmNLSOhSZypgLibcDCatV3By',
    timeout_ms:           60*1000,  // optional HTTP request timeout to apply to all requests.
    strictSSL:            true,     // optional - requires SSL certificates to be valid.
})
  
module.exports = T
