window.addEventListener("load", function() {
    const $ = django.jQuery;
    var syncTabs = function($container, lang) {
        $container.find('.translatable_field__tabs-item label:contains("'+lang+'")').each(function(){
            $(this).parents('.translatable_field').find('.translatable_field__tabs-item').removeClass('translatable_field__tabs-item_active');
            $(this).parents('.translatable_field__tabs-item').addClass('translatable_field__tabs-item_active');
            $(this).parents('.translatable_field').find('.translatable_field__widgets-item').hide();
            $('#'+$(this).attr('for')).parents('.translatable_field__widgets-item').show();
        });
    };

        $('.translatable_field__widgets-item').hide();
        // set first tab as active
        $('.translatable_field').each(function () {
            $(this).find('.translatable_field__tabs-item:first').addClass('translatable_field__tabs-item_active');
            syncTabs($(this), $(this).find('.translatable_field__tabs-item:first label').text());
        });
        // try set active last selected tab
        if (window.sessionStorage) {
            var lang = window.sessionStorage.getItem('translatable-field-lang');
            if (lang) {
                $('.translatable_field').each(function () {
                  syncTabs($(this), lang);
                });
            }
        }

        $('.translatable_field__tabs-item label').click(function(event) {
            event.preventDefault();
            syncTabs($(this).parents('.translatable_field'), $(this).text());
            if (window.sessionStorage) {
                window.sessionStorage.setItem('translatable-field-lang', $(this).text());
            }
            return false;
        });
});
