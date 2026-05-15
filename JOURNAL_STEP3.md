# Practical Task – Journal

**Student:** Didem Nur Mutlu
**Submission:** Step 3 – 15.05

---

## 1. Description of the Testing Process

Testing was performed alongside implementation, not after it. As each tool function was written, a corresponding test was added immediately to verify its behavior. This approach made it easier to catch bugs early and ensure that changes to one function did not break others.

All tests are located in `tests/test_tools.py` and target the tool functions in `tools/wardrobe_tools.py`. The tests do not require the Claude API or any network connection — they test only the pure Python logic. This keeps the test suite fast, reliable, and runnable without any credentials.

Tests are run from the project root using:

```bash
pytest tests/test_tools.py -v
```

All 11 tests pass successfully.

---

## 2. Test Scenarios

### Scenario 1 – Filter by category returns correct items
**Function:** `filter_by_category`
**Input:** Wardrobe with 4 items across 3 categories; query category `"üst"`
**Expected:** Returns exactly 2 items, both with `category == "üst"`
**Result:** ✅ Pass

### Scenario 2 – Filter is case-insensitive
**Function:** `filter_by_category`
**Input:** Query with uppercase `"ÜST"`
**Expected:** Same 2 results as lowercase query
**Result:** ✅ Pass

### Scenario 3 – Filter returns empty list for unknown category
**Function:** `filter_by_category`
**Input:** Category `"ayakkabı"` (not in wardrobe)
**Expected:** Empty list `[]`
**Result:** ✅ Pass

### Scenario 4 – List categories returns unique values
**Function:** `list_categories`
**Input:** Wardrobe with items in `"dışgiyim"`, `"üst"`, `"alt"` (some repeated)
**Expected:** List of 3 unique category names
**Result:** ✅ Pass

### Scenario 5 – List categories on empty wardrobe
**Function:** `list_categories`
**Input:** `{"clothes": []}`
**Expected:** Empty list `[]`
**Result:** ✅ Pass

### Scenario 6 – Add item increases count
**Function:** `add_item`
**Input:** Add `"Gömlek"` to `"üst"` in a wardrobe with 4 items
**Expected:** Wardrobe now contains 5 items
**Result:** ✅ Pass

### Scenario 7 – Add item assigns a unique ID
**Function:** `add_item`
**Input:** Add a new item to existing wardrobe
**Expected:** All item IDs remain unique after addition
**Result:** ✅ Pass

### Scenario 8 – Add item stores correct name and category
**Function:** `add_item`
**Input:** Add `"Şapka"` under `"aksesuar"`
**Expected:** Last item has `name == "Şapka"` and `category == "aksesuar"`
**Result:** ✅ Pass

### Scenario 9 – Remove item decreases count
**Function:** `remove_item`
**Input:** Remove item with `id == 1` from wardrobe with 4 items
**Expected:** Wardrobe now contains 3 items; success flag is `True`
**Result:** ✅ Pass

### Scenario 10 – Remove nonexistent item returns False
**Function:** `remove_item`
**Input:** Remove item with `id == 999` (does not exist)
**Expected:** Wardrobe unchanged; success flag is `False`
**Result:** ✅ Pass

### Scenario 11 – Remove item deletes the correct item
**Function:** `remove_item`
**Input:** Remove item with `id == 2`
**Expected:** No item with `id == 2` remains in wardrobe
**Result:** ✅ Pass

---

## 3. Deployment Preparation

The system is designed to run as a local command-line application. No server, database, or cloud infrastructure is required.

**Steps to run the system:**

**1. Clone the repository**
```bash
git clone https://github.com/didemio/Virtual-Wardrobe-AI.git
cd Virtual-Wardrobe-AI
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

The `requirements.txt` file contains:
```
anthropic>=0.25.0
pytest>=8.0.0
```

**3. Set the API key**

The system uses the Anthropic Claude API. An API key must be set as an environment variable before running:

```bash
# macOS / Linux
export ANTHROPIC_API_KEY=your_api_key_here

# Windows
set ANTHROPIC_API_KEY=your_api_key_here
```

**4. Run the assistant**
```bash
python agent.py
```

**5. Run the tests**
```bash
pytest tests/test_tools.py -v
```

No additional configuration is needed. The wardrobe data file (`data/wardrobe.json`) is included in the repository and is ready to use immediately.

---

## 4. Data Conversion and Porting

The system uses a JSON file (`data/wardrobe.json`) as its data source. Data passes through several transformation steps during a typical interaction.

**Input format**

The wardrobe is stored as a JSON object with a `"clothes"` array. Each item has three fields:

```json
{
  "clothes": [
    {"id": 1, "name": "Mont", "category": "dışgiyim"},
    {"id": 2, "name": "T-shirt", "category": "üst"}
  ]
}
```

**Data flow through the system**

1. **File → Python dict:** `load_wardrobe()` reads the JSON file using `json.load()` and returns a Python dictionary. This is the internal working format for all tool functions.

2. **Python dict → JSON string:** When a tool returns results to the agent, the data is serialised back to a JSON string using `json.dumps()`. This is the format the Claude API expects in `tool_result` messages.

3. **Claude API response → Python:** The agent reads the API response content blocks and extracts tool call names and inputs as Python objects.

4. **Python dict → File:** When items are added or removed, the updated dictionary is written back to `wardrobe.json` using `json.dump()`, preserving the original structure.

**Consistency measures**

- `ensure_ascii=False` is used throughout to correctly handle non-ASCII characters (e.g. Turkish letters like `ş`, `ğ`, `ü`).
- `indent=2` is used when saving to keep the file human-readable.
- IDs are assigned as `max(existing_ids) + 1` to prevent duplicates after additions.
- Category comparisons use `.lower()` to avoid case mismatch issues.
