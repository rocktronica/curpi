(function(exports, window, undefined) {

exports.IndexView = function($el) {
    var view = this;

    var _updating = null;

    $el.find("[data-action]").on("click", function() {
        var $button = $(this),
            action = $button.data("action");

        // TODO: don't need to do this every single time, especially since
        // player may not immediately be finished
        $.get("/action/" + action, function(resp){
            view.update();
        });
    });

    view.update = function(statusData) {
        if (!statusData) {
            $.getJSON("/status", view.update);
            return view;
        }

        var active = statusData.active;

        $el.find("[data-action='play']").toggle(!active);
        $el.find("[data-action='stop']").toggle(active);

        $el.find("[data-metadata]").toggle(active);

        var currentActionElement =
            "[data-action='" + (active ? "play" : "stop") + "']";
        $el.find("[data-action]")
            .removeClass("active")
            .filter(currentActionElement)
            .addClass("active")

        var metadata = statusData.metadata;
        if (!metadata) { return view; }

        $el.find("[data-metadata]").each(function() {
            var $element = $(this),
                key = $element.data("metadata"),
                fill = $element.data("metadataFill"),
                value = metadata[key];

            switch (fill) {
                case("text"):
                    $element.text(value);
                    break;
                case("src"):
                    $element
                        .attr("src", value || "")
                        .toggle(!!value);
                    break;
            }
        });

        return view;
    };

    view.autoUpdate = function(seconds) {
        _updating = window.setInterval(view.update, seconds * 1000);
    };

    return view;
};

}(this, window));
