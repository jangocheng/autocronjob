from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter

from django.urls import path, re_path
from cronjob.consumers import DagStatusConsumer, RemoteTailfLogConsumer, LocalTailfLogConsumer

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter([
            re_path(r'^ws/dagstatus/$', DagStatusConsumer),
            re_path(r'^ws/remotelog/(?P<hostname>\S+)/$', RemoteTailfLogConsumer),
            re_path(r'^ws/locallog/(?P<hostname>\S+)/$', LocalTailfLogConsumer)
        ])
    ),
    "channel": ChannelNameRouter({
        "remote-log": RemoteTailfLogConsumer,
        "local-log": LocalTailfLogConsumer,

    })
})
