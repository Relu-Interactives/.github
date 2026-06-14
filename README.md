# `.github` — Relu Interactives org profile

This is the special [`.github` repository](https://docs.github.com/en/organizations/collaborating-with-groups-in-organizations/customizing-your-organizations-profile)
for the **[Relu Interactives](https://github.com/Relu-Interactives)** GitHub organization.

GitHub renders [`profile/README.md`](profile/README.md) on the organization's public
home page at <https://github.com/Relu-Interactives>.

```
.
├── profile/
│   ├── README.md          ← shown on the org home page
│   └── assets/
│       ├── relu-banner.png  ← hero banner (generated)
│       └── relu-icon.png    ← square logo / icon
└── tools/
    └── build_banner.py    ← regenerates the hero banner (Pillow)
```

## Editing the page

Edit [`profile/README.md`](profile/README.md). Changes go live on the org home page as soon as
they land on the default branch.

## Regenerating the banner

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install Pillow
python tools/build_banner.py   # writes profile/assets/relu-banner.png
```
