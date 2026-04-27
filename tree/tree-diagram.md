# Reflection Tree — Visual Structure

The diagram below renders natively on GitHub / GitLab. It mirrors the JSON
in [`reflection-tree.json`](./reflection-tree.json). Decision nodes are
shown as diamonds; reflections as rounded grey nodes; bridges as dashed
transitions; the summary as a hexagon.

```mermaid
flowchart TD
    START([START<br/><i>greeting</i>]):::start
    %% ---------- AXIS 1: Locus ----------
    A1_OPEN[/A1_OPEN<br/>"one word for today?"/]:::question
    A1_D1{A1_D1<br/>route by word}:::decision
    A1_Q_HIGH[/A1_Q_HIGH<br/>what made it work?/]:::question
    A1_Q_LOW[/A1_Q_LOW<br/>first move when hard?/]:::question
    A1_Q2_INT[/A1_Q2_INT<br/>small unnoticed choice/]:::question
    A1_Q2_EXT[/A1_Q2_EXT<br/>where did you steer?/]:::question
    A1_D2{A1_D2<br/>internal vs external}:::decision
    A1_R_INT(A1_R_INT<br/><i>you saw your hand</i>):::reflection
    A1_R_EXT(A1_R_EXT<br/><i>still: one lever</i>):::reflection
    A1_R_MIXED(A1_R_MIXED<br/><i>both at once</i>):::reflection

    BRIDGE_1_2{{BRIDGE_1_2<br/>handled --> gave}}:::bridge

    %% ---------- AXIS 2: Orientation ----------
    A2_OPEN[/A2_OPEN<br/>giving or expecting?/]:::question
    A2_D1{A2_D1<br/>route by orientation}:::decision
    A2_Q_GIVE[/A2_Q_GIVE<br/>would you do it unseen?/]:::question
    A2_Q_EXPECT[/A2_Q_EXPECT<br/>what earned recognition?/]:::question
    A2_Q2[/A2_Q2<br/>who did you not help?/]:::question
    A2_D2{A2_D2<br/>contribution vs entitlement}:::decision
    A2_R_CONTRIB(A2_R_CONTRIB<br/><i>unowed effort</i>):::reflection
    A2_R_ENTITLE(A2_R_ENTITLE<br/><i>stop the tally</i>):::reflection
    A2_R_MIXED(A2_R_MIXED<br/><i>which did you reach for?</i>):::reflection

    BRIDGE_2_3{{BRIDGE_2_3<br/>gave --> radius}}:::bridge

    %% ---------- AXIS 3: Radius ----------
    A3_OPEN[/A3_OPEN<br/>who comes to mind?/]:::question
    A3_D1{A3_D1<br/>route by radius}:::decision
    A3_Q_SELF[/A3_Q_SELF<br/>list 3 affected/]:::question
    A3_Q_OTHERS[/A3_Q_OTHERS<br/>held someone in mind?/]:::question
    A3_Q2[/A3_Q2<br/>who would you thank?/]:::question
    A3_D2{A3_D2<br/>self / others / transcend}:::decision
    A3_R_SELF(A3_R_SELF<br/><i>look up once</i>):::reflection
    A3_R_OTHERS(A3_R_OTHERS<br/><i>you read the room</i>):::reflection
    A3_R_TRANS(A3_R_TRANS<br/><i>bigger than you</i>):::reflection

    SUMMARY{{{SUMMARY<br/><i>mirror, not grade</i>}}}:::summary
    END([END]):::endnode

    %% ---------- edges ----------
    START --> A1_OPEN --> A1_D1
    A1_D1 -- "Productive | Mixed" --> A1_Q_HIGH --> A1_Q2_INT --> A1_D2
    A1_D1 -- "Tough | Frustrating" --> A1_Q_LOW  --> A1_Q2_EXT --> A1_D2
    A1_D2 -- internal --> A1_R_INT
    A1_D2 -- external --> A1_R_EXT
    A1_D2 -- balanced --> A1_R_MIXED
    A1_R_INT   --> BRIDGE_1_2
    A1_R_EXT   --> BRIDGE_1_2
    A1_R_MIXED --> BRIDGE_1_2

    BRIDGE_1_2 --> A2_OPEN --> A2_D1
    A2_D1 -- contribution --> A2_Q_GIVE  --> A2_Q2
    A2_D1 -- entitlement --> A2_Q_EXPECT --> A2_Q2
    A2_Q2 --> A2_D2
    A2_D2 -- contribution --> A2_R_CONTRIB
    A2_D2 -- entitlement --> A2_R_ENTITLE
    A2_D2 -- balanced --> A2_R_MIXED
    A2_R_CONTRIB --> BRIDGE_2_3
    A2_R_ENTITLE --> BRIDGE_2_3
    A2_R_MIXED   --> BRIDGE_2_3

    BRIDGE_2_3 --> A3_OPEN --> A3_D1
    A3_D1 -- self --> A3_Q_SELF   --> A3_Q2
    A3_D1 -- others/transcend --> A3_Q_OTHERS --> A3_Q2
    A3_Q2 --> A3_D2
    A3_D2 -- self --> A3_R_SELF
    A3_D2 -- others --> A3_R_OTHERS
    A3_D2 -- transcend --> A3_R_TRANS
    A3_R_SELF   --> SUMMARY
    A3_R_OTHERS --> SUMMARY
    A3_R_TRANS  --> SUMMARY

    SUMMARY --> END

    classDef start      fill:#1f3a5f,stroke:#9ec5fe,color:#fff;
    classDef endnode    fill:#1f3a5f,stroke:#9ec5fe,color:#fff;
    classDef question   fill:#fff7d6,stroke:#b88a00,color:#222;
    classDef decision   fill:#ffe1e1,stroke:#b34747,color:#222;
    classDef reflection fill:#e7e3f5,stroke:#5b4ca6,color:#222;
    classDef bridge     fill:#dff4e4,stroke:#3a7d4a,color:#222,stroke-dasharray: 4 3;
    classDef summary    fill:#fde0c4,stroke:#b86b1f,color:#222;
```

## Legend

| Shape            | Meaning                                                        |
| ---------------- | -------------------------------------------------------------- |
| Stadium          | `start` / `end` — auto-advancing                               |
| Parallelogram    | `question` — fixed options, employee picks one                 |
| Diamond          | `decision` — invisible routing on prior answer or signal tally |
| Rounded box      | `reflection` — reframe text, employee reads + presses Enter    |
| Hexagon (dashed) | `bridge` — short transition between axes                       |
| Hexagon          | `summary` — end-of-session synthesis with interpolation        |

## Path counts

- 33 total nodes (start, end, summary, 2 bridges, 6 decisions, 13 questions, 9 reflections)
- 4 distinct entry-word options on Axis 1 collapse into 2 paths (`HIGH` / `LOW`)
- 3 reflection outcomes per axis (`INT` / `EXT` / `MIXED`, etc.) -> 27 reflection-triplet combinations
- Including `A1_OPEN` and `A2_OPEN` answer interpolation, the SUMMARY can render
  4 × 4 × 4 × 27 = **1,728 distinct concrete summary texts**, all from a static tree.
