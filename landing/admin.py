from django.db.models import F
from django.contrib import admin
from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    fields = ('order', 'name', 'description', 'html', 'anchor_id',)
    list_display = ('name', 'order',)
    ordering = ('order',)
    readonly_fields = ('order', 'html', 'anchor_id',)
    actions = ['move_to_top', 'move_to_bottom']

    def move_to_top(self, request, queryset):
        self.move_to_x('top', request, queryset)

    def move_to_bottom(self, request, queryset):
        self.move_to_x('bottom', request, queryset)

    def move_to_x(self, where, request, queryset):
        if len(queryset) > 1:
            self.message_user(request,
                'Please select only one service'
            )
            return

        selection = queryset.last()
        target = (where == 'top') and 1 or (
            Service.objects.order_by('order').last().order
        )

        if selection.order == target:
            self.message_user(request,
                '%s is already at the %s!' % (
                selection.name, where
            ))
            return

        if where == 'top':
            Service.objects.filter(
                order__lt=selection.order
            ).update(order=F('order') + 1)
        else:
            Service.objects.filter(
                order__gt=selection.order
            ).update(order=F('order') - 1)

        selection.order = target
        selection.save()
        self.message_user(request,
            'Successfully moved %s to the top' % selection.name
        )

    move_to_top.short_description    = 'Move Service to top'
    move_to_bottom.short_description = 'Move Service to bottom'
