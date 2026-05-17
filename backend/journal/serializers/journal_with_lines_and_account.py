from journal.serializers.journal import JournalOutputSerializer
from journal.serializers.journal_line_with_account import (
    JournalLineWithAccountSerializer,
)


class JournalWithLinesAndAccountSerializer(JournalOutputSerializer):
    lines = JournalLineWithAccountSerializer(many=True, read_only=True)

    class Meta(JournalOutputSerializer.Meta):
        fields = JournalOutputSerializer.Meta.fields + ["lines"]
