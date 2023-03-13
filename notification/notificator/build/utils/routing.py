def register_endpoints(app):
    from build.event_action import event_page
    app.register_blueprint(event_page)
