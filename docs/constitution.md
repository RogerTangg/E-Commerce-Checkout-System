# Universal Software Development Constitution
# 通用軟體開發準則

## Core Principles
## 核心原則

### I. 程式碼品質標準 (Code Quality Standards)

**MUST Requirements 必須遵守:**

- **模組化設計 (Modular Design)**: 每個功能模組必須獨立、可重用且職責單一。組件應具備明確的輸入/輸出介面 (高內聚、低耦合)。
  - Each feature module MUST be independent, reusable, and follow single responsibility principle
  - Components MUST have clear input/output interfaces (High Cohesion, Low Coupling)

- **程式碼可讀性 (Code Readability)**: 所有程式碼必須遵循專案指定的 Linter (如 ESLint, Pylint) 規範。變數、函數和組件命名必須清晰且符合語意。
  - All code MUST follow project-specific Linter standards
  - Variables, functions, and components MUST have clear, semantic names

- **型別安全 (Type Safety)**: 優先使用靜態型別語言 (如 TypeScript, Go, Rust) 或型別檢查工具確保正確性，減少執行期錯誤。
  - Prefer static typing or type checking tools to ensure type correctness
  - Minimize runtime errors through static type checking

- **錯誤處理 (Error Handling)**: 所有非同步操作、外部 API 呼叫、使用者輸入必須包含完善的錯誤處理與回饋機制 (Try-Catch/Graceful Degradation)。
  - All async operations, API calls, and user inputs MUST include comprehensive error handling
  - User-facing error messages MUST be clear and actionable

**Rationale 理由:** 高品質的程式碼是專案可維護性與可擴展性的基石。清晰的結構與規範能夠顯著降低技術債與新成員的交接成本。

---

### II. 測試標準 (Testing Standards)

**MUST Requirements 必須遵守:**

- **單元/組件測試 (Unit/Component Testing)**: 所有基礎邏輯單元或 UI 組件必須包含功能測試，驗證輸入輸出、狀態變化和邊界情況。
  - All basic logic units or UI components MUST include functional tests
  - Tests MUST verify inputs/outputs, state changes, and edge cases

- **整合測試 (Integration Testing)**: 關鍵使用者流程（如註冊登入、核心業務交易）必須包含端對端整合測試。
  - Critical user flows (e.g., auth, core transactions) MUST include E2E integration tests
  - Integration with external services MUST be tested

- **測試覆蓋率目標 (Coverage Goals)**: 核心業務邏輯的測試覆蓋率應達到 70% 以上。
  - Core business logic SHOULD achieve 70%+ test coverage
  - Focus on critical paths before edge cases

- **測試優先原則 (Test-First Principle)**: 對於關鍵功能或複雜邏輯，應先撰寫失敗的測試案例，確認需求後再實作 (TDD)。
  - For critical features, write failing tests first to confirm requirements
  - Follow Red-Green-Refactor cycle for core logic

**Rationale 理由:** 測試確保專案在快速迭代與重構過程中維持穩定性。測試不僅是驗證工具，更是確保需求被正確理解的手段。

---

### III. 使用者體驗一致性 (User Experience Consistency)

**MUST Requirements 必須遵守:**

- **設計系統 (Design System)**: 必須建立並遵循統一的設計標準（色票、字型、間距、元件樣式）。
  - MUST establish and follow unified design standards (colors, fonts, spacing, component styles)
  - Use standardized tokens or variables for consistency

- **響應式/適應性設計 (Responsive/Adaptive Design)**: 介面必須依據目標平台（Web/Mobile/Desktop）確保良好的佈局適配性。
  - Interfaces MUST ensure proper layout adaptation for target platforms
  - Use platform-appropriate approach for layout design

- **無障礙設計 (Accessibility)**: 遵循行業標準（如 WCAG 2.1 AA），確保包含鍵盤導航、螢幕閱讀器支援與足夠的對比度。
  - Follow industry standards (e.g., WCAG 2.1 AA)
  - Include keyboard navigation, screen reader support, sufficient color contrast

- **載入與回饋 (Loading & Feedback)**: 所有耗時操作必須提供載入狀態，操作結果必須有明確的成功/失敗回饋。
  - All time-consuming operations MUST show loading states
  - Operation results MUST provide clear success/failure feedback

- **一致性驗證 (Consistency Validation)**: 每個 PR 必須通過 UI/UX 一致性檢查，確保符合設計規範。
  - Every PR MUST pass UI/UX consistency checks against design specifications

**Rationale 理由:** 一致的使用者體驗能建立使用者信任，減少學習曲線。清晰的視覺引導和即時回饋是優秀軟體產品的必備條件。

---

### IV. 效能要求 (Performance Requirements)

**MUST Requirements 必須遵守:**

- **核心網頁指標 (Core Web Vitals)**: (若為 Web 專案) FCP < 1.5s, LCP < 2.5s, TTI < 3.5s。原生應用需參照相應平台標準。
  - Web projects: FCP < 1.5s, LCP < 2.5s, TTI < 3.5s. Native apps refer to platform standards
  - Optimize critical rendering path

- **資源大小優化 (Resource Optimization)**: 嚴格控制應用程式包大小 (Bundle Size)，避免載入時間過長。
  - Strictly control application bundle size
  - Use code splitting, tree shaking, and resource compression

- **API 回應時間 (API Response Time)**: 核心 API 呼叫的 P95 回應時間應低於 200ms (不含網路延遲)。
  - Core API calls SHOULD have P95 processing time < 200ms
  - Implement proper caching strategies (Client/Server side)

- **效能監控 (Performance Monitoring)**: 必須在 CI/CD 流程或正式環境中整合效能監控工具。
  - MUST integrate performance monitoring tools in CI/CD or production
  - Set up performance budgets

**Rationale 理由:** 效能直接影響使用者留存率與轉化率。效能優化應被視為功能需求的一部分，而非事後補救。

---

## 文件與註解規範 (Documentation and Comments Standards)

**Language Policy 語言政策:**

- **主要語言 (Primary Language)**: 所有文件、程式碼註解、commit message 必須以**繁體中文**為主。
  - All documentation, code comments, and commit messages MUST be primarily in **Traditional Chinese**

- **輔助語言 (Secondary Language)**: 技術術語、變數命名、關鍵概念必須使用英文或以英文標註，格式為「中文 (English)」。
  - Technical terms, naming, and key concepts MUST use English or include English in format "Chinese (English)"

**Documentation Requirements 文件要求:**

- **README.md**: 必須包含專案簡介、環境建置指南 (Setup)、技術棧說明、部署流程。
  - MUST include project overview, setup guide, tech stack explanation, deployment process

- **模組文件 (Module Documentation)**: 每個核心模組或公共組件必須包含用途說明、參數定義、使用範例。
  - Each core module or public component MUST include purpose, parameters/props definition, usage examples

- **架構文件 (Architecture Documentation)**: 資料庫結構 (Schema)、API 介面與系統架構圖必須有清楚的文件說明。
  - Database schema, API interfaces, and system architecture MUST be documented

- **內嵌註解 (Inline Comments)**: 複雜邏輯、演算法、業務規則必須有註解說明「為什麼這樣做」(Why)，而非「在做什麼」(What)。
  - Complex logic, algorithms, and business rules MUST have inline comments explaining "Why", not just "What"

**Example 範例:**

```javascript
/**
 * 處理使用者數據請求並應用過濾條件 (Process user data request and apply filters)
 * * @param {Object} request - 請求物件 (Request object)
 * @param {string} request.filterType - 過濾類型 (Filter type enum)
 * @param {boolean} request.isPremium - 是否為付費會員，影響回傳限制 (Premium status affects limits)
 * @returns {Promise<Array>} 處理後的數據陣列 (Processed data array)
 */
async function processUserData(request) {
  // 業務邏輯實作 (Implementation logic)
}
```
## 開發流程 (Development Workflow)

**Branch Strategy 分支策略:**

- **主分支 (Main Branch)**: `main` / `master` 分支為生產環境分支，必須始終保持可部署狀態。
  - `main` / `master` branch MUST always be in deployable state

- **功能分支 (Feature Branches)**: 使用 `[Issue-ID/Type-Name]` 命名格式（例如：`feat/user-auth`, `fix/login-bug`）。
  - Use standardized naming format (e.g., `feat/user-auth`, `fix/login-bug`)

- **分支生命周期 (Branch Lifecycle)**: 功能分支應短期存在，完成後立即合併並刪除。
  - Feature branches SHOULD be short-lived and deleted after merging

**Code Review 程式碼審查:**

- **必須審查 (Required Reviews)**: 所有 PR 必須至少經過一位其他成員審查後才能合併。
  - All PRs MUST be reviewed by at least one other member before merging

- **審查重點 (Review Focus)**:
  - 邏輯正確性 (Logic correctness)
  - 架構與模式 (Architecture and patterns)
  - 測試完整性 (Test completeness)
  - 安全性與效能 (Security and performance)

**Commit Standards Commit 規範:**

- **格式 (Format)**: 使用 Conventional Commits 格式：`類型(範圍): 描述`
  - Use Conventional Commits format: `type(scope): description`

- **類型 (Types)**: 
  - `feat`: 新功能 (New feature)
  - `fix`: 錯誤修復 (Bug fix)
  - `docs`: 文件更新 (Documentation update)
  - `style`: 格式調整 (Formatting, missing semi colons, etc)
  - `refactor`: 重構 (Refactoring)
  - `test`: 測試相關 (Adding missing tests, refactoring tests)
  - `chore`: 建置或工具變更 (Build tasks, package manager configs)

**Example 範例:**
```
feat(auth): 實作 JWT 驗證機制
fix(payment): 修正貨幣格式化錯誤
docs(api): 更新使用者端點說明
```

**Continuous Integration CI 流程:**

- **自動化檢查 (Automated Checks)**: 每次 PR 必須通過 Linting、測試、建置 (Build) 檢查。
  - Every PR MUST pass Linting, tests, and build checks

- **自動化部署 (CD)**: 建議合併至特定分支後自動觸發對應環境的部署。
  - Recommended to adhere to automated deployment upon merging to specific branches

**Rationale 理由:** 標準化的工作流程能夠極大化團隊協作效率，減少合併衝突，並透過自動化守門員確保程式碼庫的健康。

---

## Governance
## 治理規範

**Constitution Authority 準則權威性:**

本準則為專案開發的最高指導原則，所有開發決策必須符合準則要求。若有衝突，準則優先於其他文件或口頭慣例。

- This constitution is the highest guiding principle for project development
- All development decisions MUST comply with constitution requirements
- In case of conflicts, constitution takes precedence over other documents or conventions

**Amendment Process 修訂流程:**

- **提案 (Proposal)**: 任何團隊成員可提出修訂提案，需包含修訂理由與影響評估。
  - Any team member MAY propose amendments with rationale and impact assessment

- **討論 (Discussion)**: 修訂提案需經過團隊共識決策。
  - Amendment proposals MUST be discussed and agreed upon by the team

- **版本控制 (Versioning)**: 準則遵循語意化版本控制（Semantic Versioning）。
  - Constitution follows Semantic Versioning (MAJOR.MINOR.PATCH)

**Compliance Review 合規審查:**

- **PR 審查 (PR Review)**: 每次程式碼審查必須驗證是否符合準則要求。
  - Every code review MUST verify compliance with constitution

- **例外管理 (Exception Management)**: 若需違反準則原則（如為了解決緊急 Bug 暫時犧牲結構），必須在 PR 或程式碼中明確標註 `TODO` 與理由，並排定修復計畫。
  - If constitution principles must be violated (e.g., urgent hotfix), MUST explicitly mark with `TODO` and justification, and schedule remediation

**Migration and Propagation 遷移與傳播:**

- **模板更新 (Template Updates)**: 準則修訂後，必須同步更新專案內的相關模板檔案 (如 `plan-template.md`, `spec-template.md`, `tasks-template.md`)。
  - After constitution amendments, related template files MUST be synchronized

- **既有程式碼 (Existing Code)**: 準則修訂不強制要求立即重構既有程式碼，但新功能與重構區域必須符合新準則。
  - Constitution amendments do NOT require immediate refactoring of existing code
  - New features and refactored areas MUST comply with new constitution

**Runtime Guidance 執行期指引:**

開發過程中的具體操作指引，請參考專案內的 `.specify/templates/` (規格模板) 與 `.github/prompts/` (AI 指令) 目錄下的檔案。

- For specific operational guidance, refer to template files in `.specify/templates/` and command files in `.github/prompts/`

---

**Version**: 1.0.0 | **Status**: Active | **Last Amended**: 2025-11-24
