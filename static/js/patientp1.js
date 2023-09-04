$(document).ready(function () {

    var table



 

    

    function getPatient() {

        var settings = {
            "async": true,
            "crossDomain": true,
            "url": "patient",
            "method": "GET",
            "headers": {
                "cache-control": "no-cache"
            }
        }

        $.ajax(settings).done(function (response) {



            table = $('#datatable4').DataTable({
                "bDestroy": true,
                'paging': true, // Table pagination
                'ordering': true, // Column ordering
                'info': true, // Bottom left status text
                aaData: response,
                "aaSorting": [],
                aoColumns: [
                    {
                        mData: 'pat_id'
                    },
                    {
                        mData: 'pat_first_name'
                    },
                    {
                        mData: 'pat_last_name'
                    },
                    {
                        mData: 'pat_insurance_no'
                    },
                    {
                        mData: 'pat_address'
                    },
                    {
                        mData: 'pat_ph_no'
                    },
                    {
                        mRender: function (o) {
                            //return '<button class="btn-xs btn btn-info btn-edit" type="button">Edit</button>';
                            return '<div></div>'
                        }
                    },
                    {
                        mRender: function (o) {
                            //return '<button class="btn-xs btn btn-danger delete-btn" type="button">Delete</button>';
                            return '<div></div>'
                        }
                    }
                ]
            });
            $('#datatable4 tbody').on('click', '.delete-btn', function () {
                var data = table.row($(this).parents('tr')).data();
                console.log(data)
                deletePatient(data.pat_id)

            });
            $('.btn-edit').one("click", function (e) {
                var data = table.row($(this).parents('tr')).data();
                $('#myModal').modal().one('shown.bs.modal', function (e) {
                    for (var key in data) {
                        $("[name=" + key + "]").val(data[key])
                    }
                    $("#savethepatient").off("click").on("click", function (e) {
                        var instance = $('#detailform').parsley();
                        instance.validate()
                        console.log(instance.isValid())
                        if (instance.isValid()) {
                            jsondata = $('#detailform').serializeJSON();
                            updatePatient(jsondata, data.pat_id)
                        }

                    })
                })



            });

        });


    }




    


    getPatient()
})
