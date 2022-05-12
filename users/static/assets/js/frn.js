$(function () {

    var loadForm = function () {
      var btn = $(this);
      $.ajax({
        url: btn.attr('data-url'),
        type: 'get',
        dataType: 'json',
        beforeSend: function () {
          $("#modal-fournisseur").modal("show");
        },
        success: function (data) {
          $("#modal-fournisseur .modal-content").html(data.html_form);
        }
      });
    };
   
    var saveForm = function () {
      var form = $(this);
      $.ajax({
        url: form.attr("action"),
        data: form.serialize(),
        type: form.attr("method"),
        dataType: 'json',
        success: function (data) {
          if (data.form_is_valid) {
            $("#fournisseur-table tbody").html(data.html_fournisseur_list);
            $("#modal-fournisseur").modal("hide");
          }
          else {
            $("#modal-fournisseur .modal-content").html(data.html_form);
          }
        }
      });
      return false;
    };

    

    $(".js-load-fournisseur").click(loadForm);
    $("#modal-fournisseur").on("submit", ".js_create_fournisseur_form", saveForm);

    $("#fournisseur-table").on("click", ".js-update-fournisseur", loadForm);
    $("#modal-fournisseur").on("submit", ".js_update_fournisseur_form", saveForm);

    $("#fournisseur-table").on("click", ".js-delete-fournisseur", loadForm);
    $("#modal-fournisseur").on("submit", ".js-fournisseur-delete-form", saveForm);
  
  });
 