<!--
Sync Impact Report:
Version: 0.0.0 → 1.0.0
Reason: Initial constitution creation with comprehensive governance principles

Modified Principles:
- Added: I. 程式碼品質標準 (Code Quality Standards)
- Added: II. 測試標準 (Testing Standards)
- Added: III. 使用者體驗一致性 (User Experience Consistency)
- Added: IV. 效能要求 (Performance Requirements)

Added Sections:
- Core Principles (4 principles)
- 文件與註解規範 (Documentation and Comments Standards)
- 開發流程 (Development Workflow)
- Governance

Templates Status:
✅ plan-template.md - aligned with constitution principles
✅ spec-template.md - aligned with user story requirements
✅ tasks-template.md - aligned with testing and implementation phases
-->

# Virtual Coach App Constitution
# 虛擬健身教練應用程式開發準則

## Core Principles
## 核心原則

### I. 程式碼品質標準 (Code Quality Standards)

**MUST Requirements 必須遵守:**

- **模組化設計 (Modular Design)**: 每個功能模組必須獨立、可重用且職責單一。組件應具備明確的輸入/輸出介面。
  - Each feature module MUST be independent, reusable, and follow single responsibility principle
  - Components MUST have clear input/output interfaces

- **程式碼可讀性 (Code Readability)**: 所有程式碼必須遵循 ESLint 規範。變數、函數和組件命名必須清晰且符合語意。
  - All code MUST follow ESLint standards
  - Variables, functions, and components MUST have clear, semantic names

- **型別安全 (Type Safety)**: 優先使用 TypeScript 或 PropTypes 確保型別正確性，減少執行期錯誤。
  - Prefer TypeScript or PropTypes to ensure type correctness
  - Minimize runtime errors through static type checking

- **錯誤處理 (Error Handling)**: 所有非同步操作、API 呼叫、使用者輸入必須包含完善的錯誤處理與回饋機制。
  - All async operations, API calls, and user inputs MUST include comprehensive error handling
  - User-facing error messages MUST be clear and actionable

**Rationale 理由:** 高品質的程式碼是專案可維護性與可擴展性的基石，特別是在學生團隊環境中，清晰的程式碼結構能夠降低交接成本。

---

### II. 測試標準 (Testing Standards)

**MUST Requirements 必須遵守:**

- **組件測試 (Component Testing)**: 所有 React 組件必須包含基本功能測試，驗證渲染、狀態變化和使用者互動。
  - All React components MUST include basic functional tests
  - Tests MUST verify rendering, state changes, and user interactions

- **整合測試 (Integration Testing)**: 關鍵使用者流程（如課表生成、訓練播放）必須包含端對端整合測試。
  - Critical user flows (e.g., workout generation, training player) MUST include E2E integration tests
  - API integration with Supabase MUST be tested

- **測試覆蓋率目標 (Coverage Goals)**: 核心業務邏輯的測試覆蓋率應達到 70% 以上。
  - Core business logic SHOULD achieve 70%+ test coverage
  - Focus on critical paths before edge cases

- **測試優先原則 (Test-First Principle)**: 對於關鍵功能，應先撰寫失敗的測試案例，確認需求後再實作。
  - For critical features, write failing tests first to confirm requirements
  - Follow Red-Green-Refactor cycle for core logic

**Rationale 理由:** 測試確保專案在快速迭代中維持穩定性，並提供信心進行重構。在 MVP 階段，測試重點應放在核心功能而非追求 100% 覆蓋率。

---

### III. 使用者體驗一致性 (User Experience Consistency)

**MUST Requirements 必須遵守:**

- **設計系統 (Design System)**: 必須建立並遵循統一的設計標準（顏色、字型、間距、按鈕樣式）。
  - MUST establish and follow unified design standards (colors, fonts, spacing, button styles)
  - Use CSS variables or design tokens for consistency

- **響應式設計 (Responsive Design)**: 所有介面必須支援手機、平板、桌面裝置，確保良好的適配性。
  - All interfaces MUST support mobile, tablet, and desktop devices
  - Use mobile-first approach for layout design

- **無障礙設計 (Accessibility)**: 遵循 WCAG 2.1 AA 級標準，包含鍵盤導航、螢幕閱讀器支援、足夠的顏色對比度。
  - Follow WCAG 2.1 AA standards
  - Include keyboard navigation, screen reader support, sufficient color contrast

- **載入與回饋 (Loading & Feedback)**: 所有非同步操作必須提供載入狀態，操作結果必須有明確的成功/失敗回饋。
  - All async operations MUST show loading states
  - Operation results MUST provide clear success/failure feedback

- **一致性驗證 (Consistency Validation)**: 每個 PR 必須通過 UI 一致性檢查，確保符合設計規範。
  - Every PR MUST pass UI consistency checks against design specifications

**Rationale 理由:** 一致的使用者體驗能建立使用者信任，減少學習曲線。對於健身應用，清晰的視覺引導和即時回饋至關重要。

---

### IV. 效能要求 (Performance Requirements)

**MUST Requirements 必須遵守:**

- **首次內容繪製 (First Contentful Paint, FCP)**: 必須在 1.5 秒內完成，確保使用者快速看到內容。
  - FCP MUST complete within 1.5 seconds
  - Optimize critical rendering path

- **最大內容繪製 (Largest Contentful Paint, LCP)**: 必須在 2.5 秒內完成，確保主要內容快速載入。
  - LCP MUST complete within 2.5 seconds
  - Lazy load non-critical resources

- **互動時間 (Time to Interactive, TTI)**: 必須在 3.5 秒內可互動，確保使用者能快速操作。
  - TTI MUST be under 3.5 seconds
  - Minimize JavaScript execution time

- **包大小 (Bundle Size)**: 主要 JavaScript bundle 不得超過 250KB（gzip 壓縮後），避免載入時間過長。
  - Main JavaScript bundle MUST NOT exceed 250KB (gzipped)
  - Use code splitting and tree shaking

- **API 回應時間 (API Response Time)**: Supabase API 呼叫的 P95 回應時間應低於 200ms。
  - Supabase API calls SHOULD have P95 response time < 200ms
  - Implement proper caching strategies

- **效能監控 (Performance Monitoring)**: 使用 Lighthouse 或 Web Vitals 工具定期檢測效能指標。
  - Regularly monitor performance using Lighthouse or Web Vitals
  - Set up performance budgets in CI/CD

**Rationale 理由:** 效能直接影響使用者留存率。對於健身應用，流暢的訓練播放體驗和快速的課表生成是核心價值的一部分。

---

## 文件與註解規範 (Documentation and Comments Standards)

**Language Policy 語言政策:**

- **主要語言 (Primary Language)**: 所有文件、程式碼註解、commit message 必須以**繁體中文**為主。
  - All documentation, code comments, and commit messages MUST be primarily in **Traditional Chinese**

- **輔助語言 (Secondary Language)**: 技術術語、API 名稱、關鍵概念可以英文為輔，格式為「中文 (English)」。
  - Technical terms, API names, and key concepts MAY include English in format "Chinese (English)"

**Documentation Requirements 文件要求:**

- **README.md**: 必須包含專案簡介、快速開始指南、技術棧說明、部署流程。
  - MUST include project overview, quick start guide, tech stack explanation, deployment process

- **組件文件 (Component Documentation)**: 每個可重用組件必須包含用途說明、Props 定義、使用範例。
  - Each reusable component MUST include purpose, props definition, usage examples

- **API 文件 (API Documentation)**: 所有 Supabase 資料表結構、查詢邏輯必須有清楚的文件說明。
  - All Supabase table structures and query logic MUST be documented

- **內嵌註解 (Inline Comments)**: 複雜邏輯、演算法、業務規則必須有註解說明。避免註解顯而易見的程式碼。
  - Complex logic, algorithms, and business rules MUST have inline comments
  - Avoid commenting obvious code

**Example 範例:**

```javascript
/**
 * 根據使用者偏好生成客製化課表 (Generate customized workout plan based on user preferences)
 * 
 * @param {Object} preferences - 使用者偏好設定 (User preference settings)
 * @param {string} preferences.goal - 運動目標：'增肌' | '減脂' | '塑形' (Fitness goal)
 * @param {number} preferences.duration - 訓練時長（分鐘） (Workout duration in minutes)
 * @returns {Array} 訓練課表陣列 (Array of workout exercises)
 */
function generateWorkoutPlan(preferences) {
  // 實作邏輯 (Implementation logic)
}
```

**Rationale 理由:** 以繁體中文為主的文件能夠降低本地團隊的溝通成本，提高開發效率。同時保留英文技術術語有助於與國際開源社群接軌。

---

## 開發流程 (Development Workflow)

**Branch Strategy 分支策略:**

- **主分支 (Main Branch)**: `main` 分支為生產環境分支，必須始終保持可部署狀態。
  - `main` branch MUST always be in deployable state

- **功能分支 (Feature Branches)**: 使用 `[###-feature-name]` 命名格式（例如：`001-workout-generator`）。
  - Use `[###-feature-name]` naming format (e.g., `001-workout-generator`)

- **分支生命周期 (Branch Lifecycle)**: 功能分支應短期存在，完成後立即合併並刪除。
  - Feature branches SHOULD be short-lived and deleted after merging

**Code Review 程式碼審查:**

- **必須審查 (Required Reviews)**: 所有 PR 必須至少經過一位團隊成員審查後才能合併。
  - All PRs MUST be reviewed by at least one team member before merging

- **審查重點 (Review Focus)**:
  - 程式碼品質與可讀性 (Code quality and readability)
  - 測試覆蓋率 (Test coverage)
  - 效能影響 (Performance impact)
  - UI/UX 一致性 (UI/UX consistency)
  - 文件完整性 (Documentation completeness)

**Commit Standards Commit 規範:**

- **格式 (Format)**: 使用 Conventional Commits 格式：`類型(範圍): 描述`
  - Use Conventional Commits format: `type(scope): description`

- **類型 (Types)**: 
  - `feat`: 新功能 (New feature)
  - `fix`: 錯誤修復 (Bug fix)
  - `docs`: 文件更新 (Documentation update)
  - `style`: 程式碼格式調整 (Code style changes)
  - `refactor`: 重構 (Refactoring)
  - `test`: 測試相關 (Test-related)
  - `chore`: 建置或工具變更 (Build or tooling changes)

**Example 範例:**
```
feat(workout-generator): 新增課表生成演算法
fix(player): 修正計時器暫停問題
docs(readme): 更新部署流程說明
```

**Continuous Integration CI 流程:**

- **自動化檢查 (Automated Checks)**: 每次 PR 必須通過 ESLint、測試、建置檢查。
  - Every PR MUST pass ESLint, tests, and build checks

- **部署流程 (Deployment)**: 合併至 `main` 分支後，Render 自動觸發部署。
  - Merging to `main` automatically triggers Render deployment

**Rationale 理由:** 清晰的開發流程能夠提高團隊協作效率，減少合併衝突，確保程式碼品質。

---

## Governance
## 治理規範

**Constitution Authority 準則權威性:**

本準則為專案開發的最高指導原則，所有開發決策必須符合準則要求。若有衝突，準則優先於其他文件或慣例。

- This constitution is the highest guiding principle for project development
- All development decisions MUST comply with constitution requirements
- In case of conflicts, constitution takes precedence over other documents or conventions

**Amendment Process 修訂流程:**

- **提案 (Proposal)**: 任何團隊成員可提出修訂提案，需包含修訂理由與影響評估。
  - Any team member MAY propose amendments with rationale and impact assessment

- **討論 (Discussion)**: 修訂提案需經過至少一次團隊會議討論。
  - Amendment proposals MUST be discussed in at least one team meeting

- **版本控制 (Versioning)**: 準則遵循語意化版本控制（Semantic Versioning）：
  - MAJOR: 向後不相容的重大變更（如移除或重新定義核心原則）
  - MINOR: 新增原則、章節或重大擴充
  - PATCH: 釐清說明、用詞調整、錯字修正
  - Constitution follows Semantic Versioning:
    - MAJOR: Backward-incompatible changes (removing or redefining core principles)
    - MINOR: Adding principles, sections, or material expansions
    - PATCH: Clarifications, wording adjustments, typo fixes

**Compliance Review 合規審查:**

- **PR 審查 (PR Review)**: 每次程式碼審查必須驗證是否符合準則要求。
  - Every code review MUST verify compliance with constitution

- **定期檢討 (Periodic Review)**: 每個 Sprint 或功能發布後，團隊應檢討準則執行狀況。
  - Team SHOULD review constitution compliance after each Sprint or feature release

- **複雜度管理 (Complexity Management)**: 若需違反準則原則（如效能優化需犧牲可讀性），必須在 PR 中明確說明理由與替代方案評估。
  - If constitution principles must be violated (e.g., performance optimization sacrificing readability), MUST explicitly justify in PR with alternative evaluation

**Migration and Propagation 遷移與傳播:**

- **模板更新 (Template Updates)**: 準則修訂後，必須同步更新相關模板檔案（plan-template.md, spec-template.md, tasks-template.md）。
  - After constitution amendments, related template files MUST be synchronized

- **既有程式碼 (Existing Code)**: 準則修訂不強制要求立即重構既有程式碼，但新功能與重構必須符合新準則。
  - Constitution amendments do NOT require immediate refactoring of existing code
  - New features and refactoring MUST comply with new constitution

**Runtime Guidance 執行期指引:**

開發過程中的具體操作指引，請參考 `.specify/templates/` 目錄下的模板檔案與 `.github/prompts/` 目錄下的命令檔案。

- For specific operational guidance during development, refer to template files in `.specify/templates/` and command files in `.github/prompts/`

---

**Version**: 1.0.0 | **Ratified**: 2025-11-14 | **Last Amended**: 2025-11-14
