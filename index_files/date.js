jQuery.widget( 'gc.dateField', $.gc.stringField, {

	build: function() {
		var $input = $('<input type="text" autocomplete="off" />');
        if ( this.field.id ) {
            $input.attr('id', 'field-input-' + this.field.id);
        }
        $input.appendTo(this.inputBlock);

        var options = {
            autoclose: true,
            language: window.language,
            weekStart: 1,
            format: 'dd.mm.yyyy',
            closeOnDateSelect: true
        };

        if (this.field.settings.startDate) {
            options.startDate = this.field.settings.startDate;
        }
        if (this.field.settings.endDate) {
            options.endDate = this.field.settings.endDate;
        }

        $input.datepicker(options);

		this.input = $input;
	},

	initEditor: function( settingsEl ) {
		$.gc.stringField.prototype.initEditor.call(this, settingsEl );
	},

	getValue: function() {
		return this.input.val();
	}
} );
