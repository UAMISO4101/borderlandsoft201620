/**
 * Created by LuisSebastian on 10/8/16.
 */

$(document).ready(function () {
     $.validator.messages.required = "";
     $.validator.messages.number = "";
     $.validator.addMethod("valueNotEquals", function(value, element, arg){
        return arg !== value;
     }, "");
    $('#donation_form').validate({
        rules: {
            value: {
                required: true,
                number: true,
            },
            credit_card: {
                required: true,
                number: true,
            },
            cvc: {
                required: true,
                number: true,
            },
            month_dd: {
                valueNotEquals: "Mes",
            },
            year_dd: {
                valueNotEquals: "Año",
            },
        }, highlight: function(element) {
            $(element).parent().addClass("has-error");
        }, unhighlight: function(element) {
            $(element).parent().removeClass("has-error");
        }, errorPlacement: function(error, element) {
        },
        submitHandler: function () {
            document.getElementById("donation_form").submit();
            return false;
        }
    });

});
