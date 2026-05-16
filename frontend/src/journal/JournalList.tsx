import { JournalRow } from "./JournalRow";
import type { JournalWithLinesApi } from "./types/journalWithLines";

type JournalListProps = {
  journals: JournalWithLinesApi[] | null;
  mutate: () => void;
};

export function JournalList({ journals, mutate }: JournalListProps) {
  if (!journals || journals.length === 0) return <div className="section">仕訳データがありません。</div>;

  return (
    <div className="container">
      <h2>仕訳一覧</h2>

      <div>
        {journals.map((journal) => (
          <JournalRow 
            key={journal.id} 
            journal={journal} 
            onMutate={mutate} 
          />
        ))}
      </div>
    </div>
  );
};