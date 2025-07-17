from Bio import SeqIO

def load_sequence(path):
    """
    Загружает последовательность и фичи из файла.
    Возвращает кортеж (seq, comp, features).
    """
    print(f"[parser] load_sequence() path={path!r}")  # <<<<<< отладка
    fmt = "genbank" if path.lower().endswith((".gb", ".gbk")) else "fasta"
    print(f"[parser] detected format: {fmt}")          # <<<<<< отладка

    rec = next(SeqIO.parse(path, fmt))
    seq  = str(rec.seq)
    comp = str(rec.seq.complement())

    features = []
    if fmt == "genbank":
        for f in rec.features:
            start  = int(f.location.start)
            end    = int(f.location.end)
            strand = f.location.strand or 0
            features.append((start, end, strand, f.type))
    print(f"[parser] seq_length={len(seq)}, features_count={len(features)}")  # <<<<<<
    return seq, comp, features
