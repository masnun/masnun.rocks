+++
description = ""
author = ""
tags = ["Python", "Django"]
date = "2017-03-20T22:43:59+06:00"
title = "Django Admin: Expensive COUNT(*) Queries"

+++

If you are a Django developer, it is very likely that you use the Django Admin regularly. And if you have maintained a website with a huge amount of data, you probably already know that Django Admin can become very slow when the database table gets so large. If you log the SQL queries (either using Django logging or using Django Debug Toolbar), you would notice a very expensive 
SQL query, something like this: 

```SQL
SELECT COUNT(*) AS "__count" FROM "table_name"
```

In the default settings, you will actually notice this query twice. If you use Django Debug Toolbar, it will tell you that the query was duplicated 2 times. 

### Issue - 1

By default `ModelAdmin` has `show_full_result_count = True` which shows the full result count in the admin interface. This is the source of one of the `count(*)` queries. 

To fix that, we just need to set this on our `ModelAdmin`: 

```Python
show_full_result_count = False
```

### Issue - 2 

Even after switching `show_full_result_count` off, we are still noticing a `count(*)` query in the log. It's because the Django Paginator does a count itself. 

The solution is to somehow bypass the expensive query while still returning a number so the pagination works as expected. We can cache the count value or even run raw SQL query find an approximate value through a rather inexpensive lookup somewhere else. 

Here's a quick example of a paginator that runs the expensive query once and then caches the results: 

```Python
from django.core.paginator import Paginator
from django.core.cache import cache

# Modified version of a GIST I found in a SO thread
class CachingPaginator(Paginator):
    def _get_count(self):

        if not hasattr(self, "_count"):
            self._count = None

        if self._count is None:
            try:
                key = "adm:{0}:count".format(hash(self.object_list.query.__str__()))
                self._count = cache.get(key, -1)
                if self._count == -1:
                    self._count = super().count
                    cache.set(key, self._count, 3600)

            except:
                self._count = len(self.object_list)
        return self._count

    count = property(_get_count)

    
```

Now on our `ModelAdmin` we just need to use this paginator. 

```Python
paginator = CachingPaginator
```

Once we have done that, it will be slow when we first time load the page and it will be faster afterwards. We can also fetch and cache this value from time to time. This solution might not get us the exact count and thus mess up pagination sometimes but in most cases that would not be much 
of a problem. 
 