from alipay import AliPay

alipay_public_key_string = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAoczMn0f7kzCDGopTDH7T6VtvroeGugJRNeCMKF2MLFx9GlspQqqo978dXrtPKef5LEI2emiu/0Qv8WVKZ2hvg1bzZWpv2n7SMp7dtkaJ5tcpHJj974KvvgtZu/hZahLAMUbvlvpHxMIRdqddKvSSrhmiAcFxVkfJuXiw7XGKikx/RPR3dOPiP5rSjba4pZZ1k/aFizHNnrVEztHxU5vR2pMRmZwLv5NHMRPOj3f4r3OZeiEHQTj8QWgx0MxD8zrYucUfQ8QZOSS+mqKhJjWs1Ezs6RZnFw/ZnnDR1623roNU6IIYAYE9K0h6FYbIEcAouyGhuoWAZhi8bwH6/u6ZIwIDAQAB
-----END PUBLIC KEY-----"""
app_private_key_string = """-----BEGIN RSA PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQChzMyfR/uTMIMailMMftPpW2+uh4a6AlE14IwoXYwsXH0aWylCqqj3vx1eu08p5/ksQjZ6aK7/RC/xZUpnaG+DVvNlam/aftIynt22Ronm1ykcmP3vgq++C1m7+FlqEsAxRu+W+kfEwhF2p10q9JKuGaIBwXFWR8m5eLDtcYqKTH9E9Hd04+I/mtKNtrillnWT9oWLMc2etUTO0fFTm9HakxGZnAu/k0cxE86Pd/ivc5l6IQdBOPxBaDHQzEPzOti5xR9DxBk5JL6aoqEmNazUTOzpFmcXD9mecNHXrbeug1ToghgBgT0rSHoVhsgRwCi7IaG6hYBmGLxvAfr+7pkjAgMBAAECggEAPB+fNd0IxgQz44vdGnqSgleA46jmzn4H8W5UhrdkXCOuNToE1goWqaEx577QxvC1bdXY6pm11ZNgAWKzSEPNlE+eOGRZ1iZkM31HQ/FoUwhG9aKAUh0M8yDCoo/BoiH/mxAR/ddZDetTk/TTMSAa1WkfA2n/lKEue6Y2kLUtVwBGHUUszrpZtmB0rbl3uVm4TzoCRUJF5sTMMU48pU0H8LfEAdsQnwP8YvBxznJDBrK79O/VHAupi1EosC1bNs71GPCiBjmim72AJzpTWZRoMdSlFM/KFkAxqcQpFy34w8z0BSusnSVDdbTia2uIYETYqfqRfrdY/nos6mdblejF0QKBgQD18J6Pre3Pxj6mIverW0PlL3YP//wf/CZV9NACduAniXl3eYK92gWnmID2so3ADa3Ds5B8ViHrBdq1ov/0vrKr98Q79oKfQVGitU2xVzXOaFGaA+CtUIIHbUTvml37mkyNwqjvPTjP0h4puPj4E5ZxJib3h9bHArSz4go0AvQUiwKBgQCoaxoEdIDGKNCgHFiLT4rWr+7UmfkwsuWwe4VNfG+AwTmCTx5VpKqchvprz4r6IK/z3VYAI7Xd3vc0aNq08Gl7CsqwKYIC/RxugJxcLacODKZNonBMxpUja0tebOC6Xi4DQ9T06aTf0Hk0nfXfmERtz2nIYra3ZI5Jp/3SYxZoyQKBgQDNJ9xNBIylTr0B/5dUZPxdGVtF+4bI86DTATXnaFyR/pbJuB382vrulEO4BrhCJeb2ojp7zanbkHWiIQeclNscosEaOAc8a9N6g/z8W0ByHwk7DdMFIGxnX5oquT1+3XbQpjof35Udnyw0J63f2w8a8fV9dN4QAszUZVGXk4MiAwKBgGpcGPYvTRPXuskinZh9B0VFniKNip2CnSOzHiAtMY2yeUseBB45+7UWWRe03iPQeM4dPa6g3r3bjWp/vX7/RN37lr1huUWB626tshFUk2d//ZaRuzIBRzYzEEn1oIaR66UMNXTmCMV/tsvP5fLrCmv+zONL0/BFhMZnXRh8ky5hAoGAKV5CHHb0kBspiJodcdz+L+vGlJ/limwi5eBNF7KmkXS9SbW2A6HMNwIJZOJvMTw39nxOf/Kc+W+EWcWVvUYa+xF1um0vMu1Tx3b35I4ooywK8H72nMWJZm0H/pNFe0ElWvwbenReC3bzjOIJZ0S1DKTd9fVMGXhBd7f/W/3sUsw=
-----END RSA PRIVATE KEY-----"""

# 实例化支付应用
alipay = AliPay(
    appid="2016101000652501",
    app_notify_url=None,
    app_private_key_string=app_private_key_string,
    alipay_public_key_string=alipay_public_key_string,
    sign_type="RSA2"
)
# 发起支付请求
order_string = alipay.api_alipay_trade_page_pay(
    out_trade_no="12345",  # 订单号
    total_amount=str(10000.01),
    subject="生鲜交易",
    return_url=None,
    notify_url=None
)
print("https://openapi.alipaydev.com/gateway.do?" + order_string)
