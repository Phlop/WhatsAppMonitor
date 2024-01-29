

$(function () {

    var start_date = url_obtained_at;
    var end_date = url_end_date == '' ? url_obtained_at : url_end_date;
    var d1 = new Date(get_format_date(url_obtained_at));
    var d2 = new Date(get_format_date(end_date));

    document.getElementById("datepicker1").setAttribute("value", get_format_date(url_obtained_at));
    document.getElementById("datepicker2").setAttribute("value", get_format_date(url_end_date));

    $("#datepicker1").datepicker({

        format: "mm/dd/yyyy",
        startDate: '22/03/2018',
        endDate: last_upd_date,
        showOtherMonths: true,
        selectOtherMonths: true,
        changeMonth: true,
        changeYear: true,

    }).on("changeDate", function (e) {



        var a = $.datepicker.formatDate("yy mm dd", $(this).datepicker("getDate"));

        var b = a.split(' ');

        d1 = new Date(b);

        month = (d1.getMonth() + 1 > 9 ? "" : "0") + (d1.getMonth() + 1);

        date = (d1.getDate() > 9 ? "" : "0") + (d1.getDate());

        year = d1.getFullYear();

        today = month + "/" + date + "/" + year;
        start_date = year + "-" + month + "-" + date;
        document.getElementById("datepicker1").setAttribute("value", today);
	
	if (d1 > d2){
		end_date = year + "-" + month + "-" + date;
		document.getElementById("datepicker2").setAttribute("value",today);
	}

        $("#datepicker2").datepicker('setStartDate', d1);
    });



    $("#datepicker2").datepicker({

        format: "mm/dd/yyyy",

        startDate: d1,

        endDate: last_upd_date,

        showOtherMonths: true,

        selectOtherMonths: true,

        changeMonth: true,

        changeYear: true,

        altFormat: "DD, MM d, yy",

    }).on("changeDate", function (e) {

        var a = $.datepicker.formatDate("yy mm dd", $(this).datepicker("getDate"));

        var b = a.split(' ');

        d2 = new Date(b);

        month = (d2.getMonth() + 1 > 9 ? "" : "0") + (d2.getMonth() + 1);

        date = (d2.getDate() > 9 ? "" : "0") + (d2.getDate());

        year = d2.getFullYear();

        today = month + "/" + date + "/" + year;

        end_date = year + "-" + month + "-" + date;

        document.getElementById("datepicker2").setAttribute("value", today);

        $("#datepicker1").datepicker('setEndDate', d2);

    });



    $("#clickDate").on('click', function () {

        var oneDay = 24 * 60 * 60 * 1000;	// hours*minutes*seconds*milliseconds



        date1_field_value = document.getElementById("datepicker1").getAttribute("value").substring(0, 10);

        date2_field_value = document.getElementById("datepicker2").getAttribute("value").substring(0, 10);

        var diffDays = Math.round((new Date(date2_field_value) - new Date(date1_field_value)) / oneDay);



        document.getElementById("output").innerHTML = "Days of search:\t" + diffDays;

        document.location.href = "app.php?flag=images&obtained_at=" + start_date + "&end_date=" + end_date;

    });



});



function get_format_date(date_to_format) {

    if (date_to_format == '') {

        return get_format_date(url_obtained_at);

    }

    year = date_to_format.substring(0, 4);

    month = date_to_format.substring(5, 7);

    day = date_to_format.substring(8, 10);



    var final_date = month + "/" + day + "/" + year;



    return final_date;

}



function get_date_url_format(date_to_format) {

    return date_to_format.substring(6, 10) + '-' + date_to_format.substring(0, 2) + '-' + date_to_format.substring(3, 5);

}



function get_today() {

    var today = new Date();

    var dd = today.getDate();

    var mm = today.getMonth() + 1; //January is 0!

    var yyyy = today.getFullYear();



    if (dd < 10) {

        dd = '0' + dd;

    }



    if (mm < 10) {

        mm = '0' + mm;

    }



    today = yyyy + '-' + mm + '-' + dd;

    return today;

}

/**

$('#datepickerstart').datepicker({

//format: "dd-mm-yyyy",

todayHighlight: true,

startDate: '22-03-2018',

endDate: '-1d',

language: 'pt-BR',

// datesDisabled: ['12/04/2018']

}).on("changeDate", function (e) {

var day = (e.date.getDate() > 9 ? "" : "0") + (e.date.getDate());

var month = (e.date.getMonth() + 1 > 9 ? "" : "0") + (e.date.getMonth() + 1);

var year = e.date.getFullYear();

value_date = year + "-" + month + "-" + day;

//document.location.href = "app.php?flag=images&obtained_at=" + value_date + "&end_date=" + end_date;

});**/


