from django.http import HttpResponse
from openpyxl import Workbook
from django.apps import apps
from django.utils import timezone
import pytz
from django.db import models


def get_model_by_name(app_label, model_name):
    try:
        return apps.get_model(app_label, model_name)
    except apps.ImproperlyConfigured:
        return None


def export_to_excel(request, Model, filter_params, order_by, filename):
    # Create an Excel workbook and get the active worksheet
    wb = Workbook()
    ws = wb.active

    # Get the model's fields with their verbose names
    fields = Model._meta.get_fields()

    # Extract field names and verbose names, fallback to field name if verbose_name is not available
    field_names = []
    header_names = []
    for field in fields:
        if isinstance(field, models.Field) and field.name != 'id' and field.name != 'year':
            field_names.append(field.name)
            header_names.append(field.verbose_name if field.verbose_name else field.name)

    # Write column headers using verbose names
    ws.append(header_names)

    # Get the filtered data based on the provided filter parameters
    if filter_params:
        data = Model.objects.filter(**filter_params).order_by(*order_by)
    else:
        data = Model.objects.all()

    # Write data rows
    for row in data:
        row_data = []
        for field_name in field_names:
            field = Model._meta.get_field(field_name)
            if field.is_relation and field.many_to_one:
                related_model_value = getattr(row, field_name)
                if related_model_value is not None:
                    related_model_data = str(related_model_value)
                else:
                    related_model_data = None
                row_data.append(related_model_data)
            else:
                field_value = getattr(row, field_name)
                if isinstance(field_value, timezone.datetime):
                    # Convert datetime to the desired time zone and remove time zone information
                    field_value = field_value.astimezone(pytz.timezone('Asia/Bangkok')).replace(tzinfo=None)
                row_data.append(field_value)
        ws.append(row_data)

    # Create the HTTP response with an Excel file attachment
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    # Save the workbook to the response
    wb.save(response)
    return response


def export_by_year(request, app, model, name=None):
    app_label = app
    model_name = model
    year = request.GET.get('year')
    Model = get_model_by_name(app_label, model_name)
    if Model is not None:
        filter_params = {'year': year}
        order_by = ['Date']
        if not name:
            filename = f'{model_name}_{year}.xlsx'
        else:
            filename = f'{name}_{year}.xlsx'
        return export_to_excel(request, Model, filter_params, order_by, filename)
    else:
        raise ValueError("Model not found.")