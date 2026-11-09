# Data for the first run

## Field definitions

| CSV field | Meaning |
|---|---|
| `message_id` | Identifier within this packet; links to `raw/<message_id>.eml`. |
| `text` | Decoded subject (`Subject:`), a blank line, and the full message body. |
| `label` | Source dataset label: `spam` or `ham` (legitimate email). |

The label is not produced by our script. Do not infer it from a single word: a legitimate email can contain an advertising footer. One CSV record can span multiple lines because the text retains its paragraph breaks.

## Sources and preparation

Source: [Apache SpamAssassin public corpus](https://spamassassin.apache.org/old/publiccorpus/), archives [20030228_easy_ham.tar.bz2](https://spamassassin.apache.org/old/publiccorpus/20030228_easy_ham.tar.bz2) and [20030228_spam.tar.bz2](https://spamassassin.apache.org/old/publiccorpus/20030228_spam.tar.bz2). Prepared on 2026-10-22. The data is included locally; students do not need to download it.

Short, single-part `text/plain` messages were selected for manual inspection. This is not a random or representative sample for training or evaluating a filter. `demo.csv` and `exercise.csv` contain different messages. This historical corpus does not represent present-day email.

Transformations:

1. The selected archive members were preserved byte for byte in `raw/`, with new filenames matching `message_id`. These are originals **from the published corpus**, whose publisher had already modified some addresses and hostnames.
2. Python's standard-library `email` parser read each message using `policy.default`. The subject, body transfer encoding, and declared character encoding were decoded (ASCII when no charset was declared). Line endings were normalized to LF. Bodies were not truncated; quotations and footers were retained.
3. The `text` field was assembled as `Subject: <subject>`, two newlines, and the body. Other headers remain in the original `.eml` file, but are not included in the CSV.
4. Labels came from the archive directory: `easy_ham` → `ham`, `spam` → `spam`. Local identifiers were assigned, and the CSV files were saved as UTF-8 with LF line endings.

`manifest.json` records archive URLs and SHA-256 hashes, selected archive members, their `.eml` paths, and hashes of the originals and CSV packets. It supports reproducing the selection and checking it against the same archives. Filenames, identifiers, and labels are not input features for the future model.

## Usage terms

According to the [corpus description](https://spamassassin.apache.org/old/publiccorpus/readme.html), copyright in the message texts remains with the original senders. The SpamAssassin software license is not a license for these messages. The publisher instructs users not to send them through a live email system. In this project, we read files as text; we do not send the messages or open their links.
