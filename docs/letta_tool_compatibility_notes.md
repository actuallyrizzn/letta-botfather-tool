# Letta Custom Tool Compatibility (Self-Hosted Docker)

**Quick Rules**  
1. **Use a flat, one-line signature** with only native types:  
   ```python
   def tool_name(param1: str, flag: bool = True) -> dict:
   ```
2. **Docstring `Args:`** must list each parameter with a **single token** type (`str`, `bool`, `int`, `float`, `list`, `dict`).  
3. **Avoid** `Union[...]`, `List[...]`, multi-line signatures, or pipes in types.  
4. **Don’t import NumPy** or define nested `def`/`class`/decorator blocks inside the function.  
5. **Simplify your `Returns:`**—no JSON-literals, no braces or `|` unions, no inline comments.

---

## 1. Signature & Docstring

```python
def get_price(coin_ids: str, vs_currencies: str, include_market_cap: bool = True) -> dict:
    """
    Fetch prices from CoinGecko.

    Args:
        coin_ids (str): Comma-separated CoinGecko IDs.
        vs_currencies (str): Comma-separated target currencies.
        include_market_cap (bool): Include market-cap data.

    Returns:
        dict: Result with keys "data" on success or "error" on failure.
    """
    ...
```

- **One line** for the whole signature.  
- **`Args:`** types are plain (`str`, `bool`).  
- **Defaults** in the signature aren’t picked up by ADE; see §5.

---

## 2. Common Gotchas

### a. Complex Typing  
- **Bad:** `Union[str, List[str]]`, `List[str]`  
- **Fix:** Use `str` (and split inside your code) or manage a Pydantic model via the Python SDK.

### b. NumPy & Nested Helpers  
- **Bad:** `import numpy as np`, nested `def calculate_ema(...)`  
- **Why:** ADE validates all names at save-time → `NameError`.  
- **Fix:** Rewrite in pure Python (`statistics.mean`, loops) and inline all logic.

### c. Nested Classes & Decorators  
- **Bad:** `@dataclass class X: ...` inside your tool  
- **Why:** Decorators and inner classes also break the static parser.  
- **Fix:** Return plain dicts/lists only.

### d. Other Syntax Quirks  
- **Tuple catches:** `except (KeyError, ValueError) as e:`  
- **Comprehensions:** `prices = [p[1] for p in data]`  
- **Chained calls:** `ts = datetime.now().isoformat()`  
- **Fix:**  
  - Split exception catches into separate blocks.  
  - Use simple loops instead of comprehensions.  
  - Break chained calls into two statements.

---

## 3. Simplified `Returns:` Block

**Bad** (breaks parser):
```python
Returns:
    dict: {
        "status": "success" | "error",
        "data": {"rsi": float},  // on success
        "message": str           // on error
    }
```

**Good**:
```python
Returns:
    dict: Calculation result with keys:
        status (str): "success" or "error".
        data (dict, optional): On success, contains relevant values.
        message (str, optional): Error message.
        status_code (int, optional): HTTP code on failure.
```

---

## 4. Manual Schema Override (Optional)

If you need UI-prefilled defaults, add **below** your function:

```python
json_schema = {
    "type": "object",
    "properties": {
        "param1": {"type": "string", "description": "..."},
        "flag":   {"type": "boolean", "description": "...", "default": True},
    },
    "required": ["param1"]
}
```

Then **Save** (skip “Build schema from code”).

---

## 5. Upgrade Path

Once Letta’s parser fully supports advanced typing:

- **Union & generics** in signatures become safe.
- **Pydantic models** via `client.tools.upsert_from_function(..., args_schema=YourModel)` can replace docstring parsing entirely.
- You can reintroduce nested helpers and NumPy as long as you register via the Python SDK.

---

*Confirmed with Caren (Letta core dev) April 2025.*