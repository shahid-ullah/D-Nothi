from django.core.paginator import Paginator

from automate_process.models import UserLoginHistory
from backup_source_db.models import BackupUserLoginHistory


def backup_login_history_table():
    querysets = UserLoginHistory.objects.using('source_db').all()
    fields = [f.name for f in UserLoginHistory._meta.get_fields()]
    fields.remove('id')


    print('pagination running')
    paginator = Paginator(querysets, 10000)
    total_page = paginator.num_pages
    page_range = paginator.page_range
    print('pagination complete')

    for page_number in page_range:
        objs = paginator.page(page_number).object_list
        print(f'offices: processing page {page_number} of {total_page}')
        values = objs.values(*fields)
        batch_objects = []

        # batch_objects = [BackupUserLoginHistory(**row) for row in values]
        # batch_objects = [row for row in values]
        batch_objects = [j for j in len(values)]
        # for row in values:
        #     pass
        #     row.pop('id')
        #     last_fetch_time = row['created']
            # batch_objects.append(BackupUserLoginHistory(**row))
        # BackupUserLoginHistory.objects.using('backup_source_db').bulk_create(batch_objects)
