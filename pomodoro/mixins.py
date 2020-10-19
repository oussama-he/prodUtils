from django.contrib.messages import success


class SuccessDeletionMessageMixin(object):
    
    success_message = "Object Deleted With Success."
    
    def delete(self, request, *args, **kwargs):
        success(request, self.success_message, fail_silently=True)
        return super(SuccessDeletionMessageMixin, self).delete(request, *args, **kwargs)
