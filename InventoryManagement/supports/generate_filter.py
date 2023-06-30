from django.db.models import Q

def generate_filter(field_filters):
    filter_queries = []

    for field_filter in field_filters:
        field_name = field_filter['field_name']
        filter_input = field_filter['filter_input']
        filter_option = field_filter['filter_option']
        related_name = field_filter['related_name']

        if filter_input and filter_option:
            if filter_input == '!@':
                filter_kwargs = {
                    f'{field_name}__{related_name}__isnull' if related_name else f'{field_name}__isnull': True,
                }
            else:
                filter_kwargs = {
                f'{field_name}__{related_name}__{filter_option}' if related_name else f'{field_name}__{filter_option}': filter_input,
                }
            filter_queries.append(Q(**filter_kwargs))

    filter_query = Q()
    for query in filter_queries:
        filter_query &= query

    return filter_query