$("[data-action]").on("click", function() {
    var $button = $(this),
        action = $button.data("action");

    $.get("/action/" + action, function(resp){
        update();
    });
});

var update = function(statusData) {
    if (!statusData) {
        $.getJSON("/status", update);
        return;
    }

    $("[data-metadata]").toggle(statusData.active);

    $("[data-action]").removeClass("active");
    $("[data-action='" + (statusData.active ? "play" : "stop") + "']")
        .addClass("active")

    var metadata = statusData.metadata;
    if (!metadata) { return; }

    $("[data-metadata]").each(function() {
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
};
