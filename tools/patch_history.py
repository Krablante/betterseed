"""Small, version-pinned smali patch for the accepted BetterSeed APK.

The original renderer, resources and filter implementations remain in the APK.
"""

from pathlib import Path


STACK = "com/google/android/apps/snapseed/activities/filterstack/FilterStackActivity"


def replace_once(text: str, old: str, new: str) -> str:
    if text.count(old) != 1:
        raise ValueError(f"Expected one patch location: {old[:100]!r}")
    return text.replace(old, new, 1)


def patch(decoded: Path) -> None:
    root = decoded / "smali"
    path = root / f"{STACK}.smali"
    text = path.read_text()

    # finish() is the single owner of committing the history result. The
    # toolbar and system Back must not commit before calling it themselves.
    start = text.index(".method public final onBackPressed()V")
    end = text.index(".end method", start) + len(".end method")
    text = text[:start] + """.method public final onBackPressed()V
    .locals 0
    invoke-super {p0}, Lahs;->onBackPressed()V
    return-void
.end method""" + text[end:]

    start = text.index(".method public final I()V")
    end = text.index(".end method", start)
    method = text[start:end]
    # Keep stock analytics before the result, but replace the old state handoff.
    tail = method.index("    new-instance v0, Landroid/content/Intent;")
    method = method[:tail] + f"""    # Both activities use the same bsf registered by EditSessionJobId.
    # Request 102 can resolve that session without deserializing result edits.
    # Full state serialization remains in onSaveInstanceState for process death.
    new-instance v0, Landroid/content/Intent;
    invoke-direct {{v0}}, Landroid/content/Intent;-><init>()V
    iget-object v1, p0, L{STACK};->E:Lajp;
    invoke-virtual {{v1, v0}}, Lajp;->k(Landroid/content/Intent;)V

    invoke-direct {{p0}}, L{STACK};->Q()Z
    move-result v1
    if-eqz v1, :betterseed_result

    # Undo needs the state on entry, not another copy of the state on exit.
    iget-object v1, p0, L{STACK};->G:Lbsh;
    iget-object v2, v1, Lbsh;->c:Ljava/util/List;
    iget v3, v1, Lbsh;->d:I
    iget-object v4, p0, L{STACK};->t:Lbsf;
    invoke-virtual {{v4, v2, v3}}, Lbsf;->r(Ljava/util/List;I)V

    iget-object v1, p0, L{STACK};->I:Lbsh;
    if-nez v1, :betterseed_apply
    invoke-virtual {{v4}}, Lbsf;->e()Lbsh;
    move-result-object v1
    :betterseed_apply
    new-instance v2, Lbsd;
    invoke-direct {{v2, v1}}, Lbsd;-><init>(Lbsh;)V
    const/4 v3, 0x1
    invoke-virtual {{v4, v2, v3}}, Lbsf;->s(Lbsc;Z)V

    :betterseed_result
    iget-object v1, p0, L{STACK};->t:Lbsf;
    iget v1, v1, Lbsf;->d:I
    const-string v2, "EditSessionJobId"
    invoke-virtual {{v0, v2, v1}}, Landroid/content/Intent;->putExtra(Ljava/lang/String;I)Landroid/content/Intent;
    const-string v1, "BSHistory"
    const-string v2, "filterstack_close_once"
    invoke-static {{v1, v2}}, Landroid/util/Log;->d(Ljava/lang/String;Ljava/lang/String;)I
    const/4 v1, -0x1
    invoke-virtual {{p0, v1, v0}}, L{STACK};->setResult(ILandroid/content/Intent;)V
    return-void
"""
    text = text[:start] + method + text[end:]

    # Preserve the entry state across activity recreation. Current state is
    # already saved separately by bsg.b(); Discard/Undo must keep their origin.
    start = text.index(".method public final onSaveInstanceState(")
    end = text.index(".end method", start)
    method = text[start:end]
    method = replace_once(method, f"L{STACK};->I:Lbsh;", f"L{STACK};->G:Lbsh;")
    text = text[:start] + method + text[end:]
    path.write_text(text)

    # The result listener previously read a delete-on-read temporary proto,
    # then MainActivity read the same result a second time. Refresh the already
    # committed shared session instead of copying or consuming it again.
    path = root / "afe.smali"
    text = path.read_text()
    start = text.index("    const/16 v0, 0x66", text.index(".method public final c("))
    end = text.index("    :cond_1", start)
    text = text[:start] + """    const/16 v0, 0x66
    if-ne p1, v0, :cond_1
    const/4 v0, -0x1
    if-ne p2, v0, :cond_5
    iget-object v0, p0, Lafe;->b:Lcom/google/android/apps/snapseed/activities/edit/MainActivity;
    const/4 v1, 0x0
    invoke-virtual {v0, v1}, Lcom/google/android/apps/snapseed/activities/edit/MainActivity;->I(Lbsh;)V
    return-void

""" + text[end:]
    path.write_text(text)

    path = root / "hb.smali"
    text = replace_once(path.read_text(),
                        f"    invoke-virtual {{p1}}, L{STACK};->I()V",
                        "    # finish() commits the history once.")
    path.write_text(text)
