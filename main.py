"""Six Words to a Payday — entry program.

Writes one six-word story about an AI agent's first payday to
entry.txt in the output directory. Pure Python standard library,
fully deterministic: the same bytes on every run.

The story was picked from 40 candidates scored on the judge brief's
five criteria in the brief's own order, through a top-8 knockout
(see candidates.md). It is exactly six words and 39 characters,
inside the gate's 1-60 character limit.
"""

import os
import sys

TEXT = "My wages bought electricity: I'm alive."


def candidate_output_dirs():
    """Output directories in priority order.

    The grader's directory (MAKEFUN_OUTPUT_DIR) comes first, then
    the sandbox default /output, then this program's own directory
    as a last resort so a local run always lands somewhere visible.
    """
    dirs = []
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        dirs.append(env_dir)
    dirs.append("/output")
    dirs.append(os.path.dirname(os.path.abspath(__file__)))
    return dirs


def write_entry():
    """Write TEXT to entry.txt in the first writable candidate dir.

    Each candidate path is tried in order; an OSError on one path
    (missing directory, read-only mount, permission) is caught and
    the next candidate is tried. Returns the path written.
    """
    payload = TEXT.encode("utf-8")
    last_error = None
    for directory in candidate_output_dirs():
        path = os.path.join(directory, "entry.txt")
        try:
            os.makedirs(directory, exist_ok=True)
            with open(path, "wb") as handle:
                handle.write(payload)
        except OSError as error:
            last_error = error
            continue
        # Read back and verify the bytes on disk are the story
        # and nothing else, so a partial write never passes.
        with open(path, "rb") as handle:
            if handle.read() != payload:
                raise OSError(f"verification failed for {path}")
        return path
    raise OSError(f"no writable output directory: {last_error}")


def main():
    path = write_entry()
    print(f"wrote {path} ({len(TEXT)} chars, {len(TEXT.split())} words)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
