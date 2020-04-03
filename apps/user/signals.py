from django.db.models.signals import pre_save, post_save
from django.core.signals import request_finished
from .models import UserProfile
from log.models import OperationLog
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from log.models import HistoryLogRecords
User = get_user_model()


def get_records_log(*args, **kwargs):
    """
    id
    models
    """
    print(args[1])
    ope_type = {'~': '更新', '+': '创建', '-': '删除'}
    instance = args[1].objects.get(id=args[0])
    logs_records = instance.history.all()
    if logs_records.count() == 1:
        op_user, op_type, msg = '', '', ''
        for history in logs_records:
            op_user = history.history_user.username
            op_type = ope_type[history.history_type]
            msg = "创建'%s'" % history.username
        return {"op_user": op_user, "op_type": op_type, "op_msg": msg}
    else:
        new_record, old_record, *_ = logs_records
        delta = new_record.diff_against(old_record)
        msg = ''
        for change in iter(delta.changes):
            if change.field == 'password':
                msg += "变更密码; "
            else:
                msg += "字段'{}'内容由'{}'变更为'{}'; ".format(change.field, change.old, change.new)
        return {
            "op_user": new_record.history_user.username,
            "op_type": ope_type[new_record.history_type],
            "op_msg": msg}


@receiver(post_save, sender=User)
def save_create_userprofile(sender, instance, created, **kwargs):
    if instance.last_login == None:
        HistoryLogRecords.objects.create(**get_records_log(instance.id, User))
    else:
        # login action, no records
        print('user login')
        pass

