from journal.serializers.journal_line import JournalLineOutputSerializer
from management.serializers.account import AccountOutputSerializer


class JournalLineWithAccountSerializer(JournalLineOutputSerializer):
    account = AccountOutputSerializer(read_only=True)

    class Meta(JournalLineOutputSerializer.Meta):
        fields = JournalLineOutputSerializer.Meta.fields + ["account"]
