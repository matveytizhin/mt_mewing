jQuery.widget('gc.phoneConfirmField', $.gc.abstractField, {
    phone: null,

    build: function () {
        var captchaEnabled = !window.disableCaptchaForConfirmPhone;

        if (captchaEnabled) {
            $('<script type="text/javascript" src="https://www.google.com/recaptcha/api.js"></script>').appendTo($('body'));
        }

        this.input = $( '<input type="text" name="' +  this.options.field.fieldName + '" size=4 placeholder="Введите код подтверждения"/>')
        this.codeSentEl = $( "<div>Код подтверждения был отправлен на ваш номер</div>");
        this.input.hide();
        this.codeSentEl.hide();

        this.buttonsEl = $('<div style="padding-top: 10px; padding-bottom: 10px;"/>');

        if (captchaEnabled) {
            this.captcha = $('<div class="g-recaptcha" data-sitekey="6LedcXoUAAAAALSIjF8UgtAgz0J6JwkbFW2mZiTI"></div>');
            this.captcha.appendTo(this.buttonsEl);
        }

        this.sendSmsLink = $( "<a href='javascript:void(0)' class='btn btn-sm btn-primary' style='margin-right: 10px;'>Получить код</a>");
        this.sendSmsLink.appendTo( this.buttonsEl );

        this.buttonsEl.appendTo( this.inputBlock );
        this.codeSentEl.appendTo( this.inputBlock );
        this.input.appendTo( this.inputBlock );

		if (this.field.showResendCode) {
			var resendCodeLinkLabel = 'Отправить код повторно';
			if (typeof Yii != 'undefined') {
				resendCodeLinkLabel = Yii.t('cms', 'Отправить код повторно');
			}
			this.resendCodeLink = $('<div class="repeat-confirm-code"><a href="#" class="repeat-confirm-code-btn">'
				+ resendCodeLinkLabel + '</a></div>');
			this.resendCodeLink.hide();
			this.resendCodeLink.appendTo(this.inputBlock);
		}

        var self = this;
        this.sendSmsLink.click( function() {
            self.phone = $('input.form-field-phone').val();
            var data = {phone: self.phone};
            if (captchaEnabled) {
                data.recaptcha = grecaptcha.getResponse();
            }
            ajaxCall( "/user/public/user/sendConfirmationCode", data, { btn: $(this) }, function( response ) {
                self.valueChanged(1);
                self.sendSmsLink.hide();
                if (response.text) {
                    $.toast(response.text, {type: "info"});
                }
            } );
            return false;
        });

		if (this.field.showResendCode) {
			this.resendCodeLink.click(function (event) {
				event.preventDefault();
				var data = {phone: self.phone, resend: 1};
				if (captchaEnabled) {
					data.recaptcha = grecaptcha.getResponse();
				}
				ajaxCall("/user/public/user/sendConfirmationCode", data, {btn: $(this)}, function (response) {
					if (response.text) {
						$.toast(response.text, {type: "info"});
					}
				});
				return false;
			});
		}
        $('form.xdget-block').find('.form-field-phone').on('keyup change click input', function() {
            if (grecaptcha && captchaEnabled) {
                grecaptcha.reset();
            }
        });
    },
    getValue: function () {
        return [
            this.input.val()
        ].join(':');
    },
    valueChanged: function( value, otherValues ) {
        if ( otherValues ) {
            this.phone = otherValues.phone;
        }
        if ( value == 1 ) {
            this.sendSmsLink.hide();
            this.codeSentEl.show();
            this.input.show();
			if (this.field.showResendCode) {
				this.resendCodeLink.show();
			}
        }

        this.input.val( "" );

        if (
			(typeof otherValues != 'undefined')
			&& otherValues.phone_confirmed == true
            && (this.input.is(":visible") == false)
            && (this.options.field.required == 'true')
        ) {
            this.input.val(otherValues.phone_confirmed);
        }
    }
});
