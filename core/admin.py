from django.contrib import admin
from django.urls import path, reverse
from django.utils.html import format_html
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from .models import ServiceCategory, Service, ContactMessage


# =========================================================
# SERVICE CATEGORY
# =========================================================

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):

    list_display = (
        "name",
    )

    search_fields = (
        "name",
    )

    fields = (
        "name",
        "description",
        "image",
    )


# =========================================================
# SERVICE
# =========================================================

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "category",
        "price",
        "duration",
        "is_active",
    )

    list_filter = (
        "category",
        "is_active",
    )

    search_fields = (
        "name",
    )

    list_editable = (
        "price",
        "is_active",
    )


# =========================================================
# CUSTOMER ENQUIRIES
# =========================================================

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "email",
        "phone",
        "created_at",
        "read_status",
    )

    list_filter = (
        "is_read",
        "created_at",
    )

    search_fields = (
        "name",
        "email",
        "phone",
        "message",
    )

    readonly_fields = (
        "name",
        "email",
        "phone",
        "message",
        "created_at",
    )

    fields = (
        "name",
        "email",
        "phone",
        "message",
        "created_at",
    )

    # -----------------------------------------------------
    # Customer enquiry detail page
    # -----------------------------------------------------

    def changeform_view(
        self,
        request,
        object_id=None,
        form_url="",
        extra_context=None,
    ):

        extra_context = extra_context or {}

        extra_context["show_save"] = False
        extra_context["show_save_and_continue"] = False
        extra_context["show_save_and_add_another"] = False
        extra_context["show_delete"] = False

        return super().changeform_view(
            request,
            object_id,
            form_url,
            extra_context=extra_context,
        )

    def change_view(
        self,
        request,
        object_id,
        form_url="",
        extra_context=None,
    ):

        extra_context = extra_context or {}

        extra_context["title"] = "Customer Enquiry"

        return super().change_view(
            request,
            object_id,
            form_url,
            extra_context=extra_context,
        )

    # -----------------------------------------------------
    # Read / Unread status
    # -----------------------------------------------------

    @admin.display(description="IS READ")
    def read_status(self, obj):

        if obj.is_read:

            return format_html(
                '<a href="{}" class="lumera-read-status read">✓</a>',
                reverse(
                    "admin:contactmessage_toggle_read",
                    args=[obj.id],
                ),
            )

        return format_html(
            '<a href="{}" class="lumera-read-status unread">✕</a>',
            reverse(
                "admin:contactmessage_toggle_read",
                args=[obj.id],
            ),
        )

    # -----------------------------------------------------
    # Custom toggle-read URL
    # -----------------------------------------------------

    def get_urls(self):

        urls = super().get_urls()

        custom_urls = [
            path(
                "<int:message_id>/toggle-read/",
                self.admin_site.admin_view(
                    self.toggle_read
                ),
                name="contactmessage_toggle_read",
            ),
        ]

        return custom_urls + urls

    # -----------------------------------------------------
    # Toggle read/unread WITHOUT page reload
    # -----------------------------------------------------

    def toggle_read(self, request, message_id):

        message = get_object_or_404(
            ContactMessage,
            id=message_id,
        )

        message.is_read = not message.is_read

        message.save(
            update_fields=["is_read"]
        )

        return JsonResponse({
            "success": True,
            "is_read": message.is_read,
        })


# =========================================================
# LUMÉRA ADMIN BRANDING
# =========================================================

admin.site.site_header = "LUMÉRA"
admin.site.site_title = "Luméra Salon & Spa"
admin.site.index_title = "Administration"