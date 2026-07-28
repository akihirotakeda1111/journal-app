import "./styles/journal.css";
import "./styles/modal.css";
import "./styles/row.css";
import "./styles/tab.css";
import { useState } from "react";
import { JournalForm } from "./journal/components/JournalForm";
import { JournalList } from "./journal/components/JournalList";
import { TrialBalance } from "./journal/components/TrialBalance";
import useSWR from "swr";
import { createValidatedArrayFetcher } from "./utils/api/fetchValidated";
import {
  JournalWithLinesApiSchema,
  type JournalWithLinesApi,
} from "./journal/schemas";

const fetchJournals = createValidatedArrayFetcher(JournalWithLinesApiSchema);

function App() {
  const [activeTab, setActiveTab] = useState<"journal" | "trial">("journal");
  const [refreshKey, setRefreshKey] = useState(0);

  const openTrialBalance = () => {
    setActiveTab("trial");
    setRefreshKey((prev) => prev + 1);
  };

  const { data: journals, error, isLoading, mutate } = useSWR<JournalWithLinesApi[]>(
    "/journal/list/",
    fetchJournals
  );

  if (isLoading) return <div>読み込み中...</div>;
  if (error) return <div>{error.message}</div>;

  return (
    <div className="app-container">

      {/* --- タブメニュー --- */}
      <div className="tab-bar">
        <button
          className={`tab-item ${activeTab === "journal" ? "active" : ""}`}
          onClick={() => setActiveTab("journal")}
        >
          仕訳入力・一覧
        </button>

        <button
          className={`tab-item ${activeTab === "trial" ? "active" : ""}`}
          onClick={openTrialBalance}
        >
          残高試算表
        </button>
      </div>

      <div className="tab-content">
        {activeTab === "journal" && (
          <>
            <JournalForm mode="create" mutate={mutate} onDone={() => {}} />
            <JournalList journals={journals ?? []} mutate={mutate} />
          </>
        )}

        {activeTab === "trial" && <TrialBalance refreshKey={refreshKey} />}
      </div>
    </div>
  );
}

export default App;
