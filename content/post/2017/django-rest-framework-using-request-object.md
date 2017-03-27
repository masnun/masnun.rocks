+++
date = "2017-03-27T12:49:01+06:00"
description = ""
author = ""
tags = ["Python", "Django", "Django REST Framework"]
title = "Django REST Framework: Using the request object"

+++

While working with [Django REST Framework](http://www.django-rest-framework.org/) aka DRF, we often wonder how to customize our response based on request parameters. May be we want to check something against the logged in user (`request.user`) ? Or may be we want to modify part of our response based on a certain request parameter? How do we do that? We will discuss a few use cases below. 

## ModelViewSet - Filtering based on `request`

This is very often required while using `ModelViewSet`s. We have many `Item`s in our database. But when listing them, we only want to display the items belonging to the current logged in user. 

```python
from rest_framework.permissions import IsAuthenticated

class ItemViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ItemSerializer

    def get_queryset(self):
        queryset = Item.objects.all().filter(user=request.user)

        another_param = self.request.GET.get('another_param')
        if another_param:
            queryset = queryset.filter(another_field=another_param)

        return queryset
```


If you are using the awesome `ModelViewSet`, you can override the `get_queryset` method. Inside it, you can access the `request` object as `self.request`. In the above example, we are only listing the items which has our current user set as their `user` field. At the same time, we are also filtering the queryset based on another parameter. Basically you have the queryset and `self.request` available to you, feel free to use your imagination to craft all the queries you need!

## Serializers - Modifying Response based on `request` 

What if we don't want to display `item_count` for the users by default? What if we only want to display that field when a request parameter, `show_count` is set? We can override the serializer to do that. 

```python
class UserSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        context = kwargs.get('context', None)
        if context:
            request = kwargs['context']['request']

            show_count = request.GET.get('show_count')
            if show_count:
                self.fields['item_count'] = IntegerField(source="item_count")
```

When Serializers are constructed by DRF, it gets the `request` in the `context`. So we should always check if it exists and use it as needed. We can override the serializer fields by accessing `self.fields`. 

Please note: The `request` object will be passed only if DRF constructs the serializer for you, for example when you just pass the `serializer_class` to a `ModelViewSet`. But if you are using the Serializer in your custom views, please do remember to pass the request manually, otherwise it won't work. 

```python
item_serializer = ItemSerializer(item, context={"request": request})
```

In our case we have just used `IntegerField`. You can of course use another serializer to embed the full data of a related field. 

## Using `request` in Serializer Fields 

Serializer fields have `context` too! 

```python
class ShortURLField(ReadOnlyField):
    def to_representation(self, value):
        return self.context['request'].build_absolute_uri(value)
```

and here's the serializer: 

```py
class URLSerializer(ModelSerializer):
    short_url = ShortURLField()

    class Meta:
        model = URL
        fields = "__all__"

```

In the `URL` model, there is a method named `short_url` that returns a slug for that url. In our custom `ShortURLField`, we have customized the `to_representation` method to use the `build_absolute_uri(value)` method on current request for creating the full url from the slug.