$(document).ready(function () {

    var table


   


    function updateMedication(data, code) {
        var settings = {
            "async": true,
            "crossDomain": true,
            "url": "medication/" + code,
            "method": "PUT",
            "headers": {
                "content-type": "application/json",
                "cache-control": "no-cache"
            },
            "processData": false,
            "data": JSON.stringify(data)
        }

        $.ajax(settings).done(function (response) {
            $('.modal.in').modal('hide')
            $.notify("Medicine Updated Successfully", {"status":"success"});
            table.destroy();
            $('#datatable4 tbody').empty(); // empty in case the columns change
            getMedication()
        });


    }

    function getMedication() {

        var settings = {
            "async": true,
            "crossDomain": true,
            "url": "medication",
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
                    mData: 'code'
                },
                {
                    mData: 'name'
                },
                {
                    mData: 'brand'
                },
                {
                    mData: 'description'
                },
                {
                    mRender: function (o) {
                        // return '<button class="btn-xs btn btn-info btn-edit" type="button">Edit</button>';
                        return '<div></div>'
                    }
                },
                {
                    mRender: function (o) {
                        // return '<button class="btn-xs btn btn-danger delete-btn" type="button">Delete</button>';
                        return '<div></div>'
                    }
                }
                ]
            });
            $('#datatable4 tbody').on('click', '.delete-btn', function () {
                var data = table.row($(this).parents('tr')).data();
                console.log(data)
                deleteMedication(data.code)

            });
            $('.btn-edit').one("click", function(e) {
                var data = table.row($(this).parents('tr')).data();
                $('#myModal').modal().one('shown.bs.modal', function (e) {
                    for (var key in data) {
                        $("[name=" + key + "]").val(data[key])
                    }
                    $("#savethemedication").off("click").on("click", function(e) {
                        var instance = $('#detailform').parsley();
                        instance.validate()
                        console.log(instance.isValid())
                        if(instance.isValid()){
                            jsondata = $('#detailform').serializeJSON();
                            updateMedication(jsondata, data.code)
                        }

                    })
                })



            });

        });


    }




    $("#addMedication").click(function () {
        $('#detailform input,textarea').val("")
        $('#myModal').modal().one('shown.bs.modal', function (e) {

            console.log('innn')
            $("#savethemedication").off("click").on("click", function(e) {
                console.log("inn")
                var instance = $('#detailform').parsley();
                instance.validate()
                if(instance.isValid()){
                    jsondata = $('#detailform').serializeJSON();
                    addMedication(jsondata)
                }

            })

        })



    })


    getMedication()
})
