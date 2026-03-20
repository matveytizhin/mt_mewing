/* jshint esversion: 6 */
class PaymentWidget {
    static open(dealId, params = {}) {
        document.dispatchEvent(
            new CustomEvent('payment-init', {
                detail: {
                    dealId: dealId,
                    params: params
                }
            })
        );
    }
}
